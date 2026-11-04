import glob
import os
import signal
import struct
import sys
import threading
from time import sleep

import serial
from serial.tools import list_ports

try:
    import hid
except ImportError:
    hid = None

# Known USB Vendor IDs commonly used by Makeblock mBot (CH340G, FTDI, CP210x)
MBOT_USB_VIDS = {0x1A86, 0x0403, 0x10C4}


class mSerial:
    ser = None

    def __init__(self):
        self.ser = None

    def start(self, port=None, baudrate=115200, timeout=0.1):
        resolved_port = port if (port and port != "auto") else self.autoDetectPort()
        if not resolved_port:
            raise OSError(
                "No mBot serial port detected. Connect your mBot via USB (and switch it ON) "
                "or pass the port explicitly, e.g. mbot(port='/dev/ttyUSB0') or mbot(port='COM3')."
            )
        self.ser = serial.Serial(resolved_port, baudrate, timeout=timeout)

    def device(self):
        return self.ser

    def autoDetectPort(self):
        env_port = os.environ.get("MBOT_PORT")
        if env_port:
            return env_port

        ports = list(list_ports.comports())
        # First pass: look for known mBot USB-serial bridge VIDs (e.g. CH340 0x1A86)
        for info in ports:
            if getattr(info, "vid", None) in MBOT_USB_VIDS:
                return info.device

        # Second pass: look for typical USB serial device names
        for info in ports:
            dev = info.device or ""
            desc = (info.description or "").lower()
            if any(
                token in dev.lower() or token in desc
                for token in ("ch340", "ch341", "usbserial", "wchusbserial", "ttyusb", "ttyacm")
            ):
                return dev

        # Fallback to first enumerated non-virtual port if any exist
        for info in ports:
            if info.device and not info.device.startswith("/dev/ttyS"):
                return info.device

        discovered = self.serialPorts()
        return discovered[0] if discovered else None

    def serialPorts(self):
        if sys.platform.startswith("win"):
            ports = [f"COM{i + 1}" for i in range(256)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.wchusbserial*") + glob.glob("/dev/tty.usbserial*")
        else:
            raise OSError("Unsupported platform")
        result = []
        for port in ports:
            try:
                s = serial.Serial()
                s.port = port
                s.close()
                result.append(port)
            except Exception:
                continue
        return result

    def writePackage(self, package):
        if self.ser is not None and self.isOpen():
            self.ser.write(bytes(package))
            sleep(0.01)

    def read(self):
        if self.ser is None:
            return b""
        return self.ser.read(1)

    def isOpen(self):
        if self.ser is None:
            return False
        return bool(getattr(self.ser, "is_open", False))

    def inWaiting(self):
        if self.ser is None or not self.isOpen():
            return 0
        return int(getattr(self.ser, "in_waiting", 0))

    def close(self):
        if self.ser is not None and self.isOpen():
            self.ser.close()


class mHID:
    def __init__(self):
        self.device = None
        self.buffer = []
        self.bufferIndex = 0
        self._open = False

    def start(self, vid=0x0416, pid=0xFFFF):
        if hid is None:
            raise ImportError(
                "hidapi is required for startWithHID(). "
                "Install with: pip install 'python-for-mbot[hid]'"
            )
        self.device = hid.device()
        self.device.open(vid, pid)
        self.buffer = []
        self.bufferIndex = 0
        self._open = True

    def enumerate(self):
        if hid is None:
            return []
        return hid.enumerate()

    def writePackage(self, package):
        if self.device is None:
            return
        buf = [0, len(package)] + [int(b) & 0xFF for b in package]
        self.device.write(buf)
        sleep(0.01)

    def read(self):
        c = self.buffer[0]
        self.buffer = self.buffer[1:]
        return bytes([c & 0xFF])

    def isOpen(self):
        return self._open and self.device is not None

    def inWaiting(self):
        if not self.isOpen():
            return 0
        buf = self.device.read(64)
        length = buf[0] if len(buf) > 0 else 0
        if length > 0:
            for i in range(min(length, len(buf) - 1)):
                self.buffer.append(buf[i + 1] & 0xFF)
        return len(self.buffer)

    def close(self):
        if self.device is not None and self._open:
            self._open = False
            self.device.close()


class mLoopback:
    """In-memory transport for classroom simulation and offline testing (MBOT_SIMULATE=1)."""

    def __init__(self):
        self.sent_packages = []
        self.rx_buffer = bytearray()
        self.sensor_overrides = {}
        self._open = False

    def start(self):
        self._open = True

    def set_sensor_value(self, device_id, value):
        self.sensor_overrides[int(device_id)] = value

    def writePackage(self, package):
        data = bytearray(package)
        self.sent_packages.append(data)
        # If this is a GET sensor request (0xFF 0x55 len extID 0x01 device ...),
        # synthesize a realistic float response frame so synchronous queries work in simulation.
        if len(data) >= 6 and data[0] == 0xFF and data[1] == 0x55 and data[4] == 0x01:
            ext_id = data[3]
            device_id = data[5]
            override = self.sensor_overrides.get(device_id)
            if isinstance(override, list) and override:
                val = override.pop(0) if len(override) > 1 else override[0]
            elif override is not None:
                val = override
            else:
                val = 0 if device_id == 0x1F else 42.0

            if device_id == 0x1F:  # BUTTON_INNER -> byte (type 1)
                self.queueResponse(ext_id, 1, [int(bool(val))])
            else:  # float sensor response (type 2)
                self.queueResponse(ext_id, 2, list(struct.pack("<f", float(val))))

    def queueResponse(self, ext_id, data_type, payload_bytes):
        frame = bytearray([0xFF, 0x55, ext_id & 0xFF, data_type & 0xFF])
        frame.extend(int(b) & 0xFF for b in payload_bytes)
        frame.extend([0x0D, 0x0A])
        self.rx_buffer.extend(frame)

    def read(self):
        if not self.rx_buffer:
            return b""
        b = self.rx_buffer[0]
        del self.rx_buffer[0]
        return bytes([b])

    def isOpen(self):
        return self._open

    def inWaiting(self):
        return len(self.rx_buffer)

    def close(self):
        self._open = False


class mBot:
    def __init__(self, auto_connect=False, port=None, use_hid=False, simulate=None):
        self._lock = threading.Lock()
        self.__selectors = {}
        self._sync_events = {}
        self._sync_results = {}
        self._next_ext_id = 80
        self.buffer = []
        self.bufferIndex = 0
        self.isParseStart = False
        self.exiting = False
        self.isParseStartIndex = 0
        self.device = None
        self._reader_thread = None
        self.command_log = []

        if threading.current_thread() is threading.main_thread():
            try:
                signal.signal(signal.SIGINT, self.exit)
            except ValueError:
                pass

        if simulate is None:
            simulate = os.environ.get("MBOT_SIMULATE", "").lower() in ("1", "true", "yes")

        if auto_connect:
            self.connect(port=port, use_hid=use_hid, simulate=simulate)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.device is not None and self.device.isOpen():
                self.doMove(0, 0)
                self.doBuzzer(0, 0)
                self.doRGBLedOnBoard(0, 0, 0, 0)
        except Exception:
            pass
        self.close()
        return False

    def connect(self, port=None, use_hid=False, simulate=False):
        if simulate:
            self.device = mLoopback()
            self.device.start()
            self.start()
            return
        if use_hid:
            self.startWithHID()
        else:
            self.startWithSerial(port)

    def startWithSerial(self, port=None):
        self.device = mSerial()
        self.device.start(port)
        self.start()
        return True

    def startWithHID(self):
        self.device = mHID()
        self.device.start()
        self.start()
        return True

    def excepthook(self, exctype, value, traceback):
        self.close()

    def start(self):
        self.exiting = False
        sys.excepthook = self.excepthook
        if self._reader_thread is None or not self._reader_thread.is_alive():
            self._reader_thread = threading.Thread(
                target=self.__onRead, args=(self.onParse,), daemon=True
            )
            self._reader_thread.start()

    def close(self):
        self.exiting = True
        if self.device is not None:
            try:
                self.device.close()
            except Exception:
                pass
        if (
            self._reader_thread is not None
            and self._reader_thread.is_alive()
            and threading.current_thread() is not self._reader_thread
        ):
            self._reader_thread.join(timeout=0.3)

    def exit(self, sig, frame):
        self.close()
        sys.exit(0)

    def __onRead(self, callback):
        while not self.exiting:
            try:
                if self.device is not None and self.device.isOpen():
                    n = self.device.inWaiting()
                    for _ in range(n):
                        raw = self.device.read()
                        if raw:
                            r = raw[0] if isinstance(raw, (bytes, bytearray)) else ord(raw)
                            callback(r)
                    sleep(0.01)
                else:
                    sleep(0.1)
            except Exception:
                if self.exiting:
                    break
                sleep(0.1)

    def __writePackage(self, pack):
        if self.device is not None:
            self.device.writePackage(pack)

    @staticmethod
    def _clamp_byte(val):
        return max(0, min(255, int(val)))

    def clear_command_log(self):
        """Clear the recorded high-level command history."""
        self.command_log.clear()

    def set_simulated_sensor(self, sensor_name, value):
        """Configure simulated sensor return value(s) when running with `mbot(simulate=True)`.

        `sensor_name` may be `'ultrasonic'`/`'distance'`, `'light'`, `'line_follower'`, or
        `'button'`. `value` may be a single float/int or a list of values to return on
        successive reads.
        """
        sensor_map = {
            "ultrasonic": 0x01,
            "distance": 0x01,
            "light": 0x03,
            "line_follower": 0x11,
            "button": 0x1F,
        }
        key = str(sensor_name).lower().strip()
        if key not in sensor_map:
            raise ValueError(f"Unknown sensor '{sensor_name}'. Expected one of {list(sensor_map)}")
        if isinstance(self.device, mLoopback):
            self.device.set_sensor_value(sensor_map[key], value)

    def doRGBLed(self, port, slot, index, red, green, blue):
        r = self._clamp_byte(red)
        g = self._clamp_byte(green)
        b = self._clamp_byte(blue)
        self.command_log.append(
            {
                "action": "rgb_led",
                "port": self._clamp_byte(port),
                "slot": self._clamp_byte(slot),
                "index": self._clamp_byte(index),
                "r": r,
                "g": g,
                "b": b,
            }
        )
        self.__writePackage(
            bytearray(
                [
                    0xFF,
                    0x55,
                    0x09,
                    0x00,
                    0x02,
                    0x08,
                    self._clamp_byte(port),
                    self._clamp_byte(slot),
                    self._clamp_byte(index),
                    r,
                    g,
                    b,
                ]
            )
        )

    def doRGBLedOnBoard(self, index, red, green, blue):
        self.doRGBLed(0x07, 0x02, index, red, green, blue)

    def doMotor(self, port, speed):
        self.command_log.append(
            {"action": "motor", "port": self._clamp_byte(port), "speed": int(speed)}
        )
        self.__writePackage(
            bytearray(
                [0xFF, 0x55, 0x06, 0x00, 0x02, 0x0A, self._clamp_byte(port)]
                + self.short2bytes(speed)
            )
        )

    def doMove(self, leftSpeed, rightSpeed):
        self.command_log.append(
            {"action": "move", "left": int(leftSpeed), "right": int(rightSpeed)}
        )
        self.__writePackage(
            bytearray(
                [0xFF, 0x55, 0x07, 0x00, 0x02, 0x05]
                + self.short2bytes(-int(leftSpeed))
                + self.short2bytes(int(rightSpeed))
            )
        )

    def doServo(self, port, slot, angle):
        self.command_log.append(
            {
                "action": "servo",
                "port": self._clamp_byte(port),
                "slot": self._clamp_byte(slot),
                "angle": self._clamp_byte(angle),
            }
        )
        self.__writePackage(
            bytearray(
                [
                    0xFF,
                    0x55,
                    0x06,
                    0x00,
                    0x02,
                    0x0B,
                    self._clamp_byte(port),
                    self._clamp_byte(slot),
                    self._clamp_byte(angle),
                ]
            )
        )

    def doBuzzer(self, buzzer, time=0):
        self.command_log.append(
            {"action": "buzzer", "frequency_hz": int(buzzer), "duration_ms": int(time)}
        )
        self.__writePackage(
            bytearray(
                [0xFF, 0x55, 0x07, 0x00, 0x02, 0x22]
                + self.short2bytes(int(buzzer))
                + self.short2bytes(int(time))
            )
        )

    def doSevSegDisplay(self, port, display):
        self.__writePackage(
            bytearray(
                [0xFF, 0x55, 0x08, 0x00, 0x02, 0x09, self._clamp_byte(port)]
                + self.float2bytes(display)
            )
        )

    def doIROnBoard(self, message):
        if isinstance(message, str):
            msg_bytes = list(message.encode("utf-8"))
        elif isinstance(message, (bytes, bytearray, list, tuple)):
            msg_bytes = [int(b) & 0xFF for b in message]
        else:
            msg_bytes = [int(message) & 0xFF]
        self.__writePackage(
            bytearray([0xFF, 0x55, len(msg_bytes) + 3, 0x00, 0x02, 0x0D] + msg_bytes)
        )

    def requestLightOnBoard(self, extID, callback):
        self.requestLight(extID, 8, callback)

    def requestLight(self, extID, port, callback):
        self.__doCallback(extID, callback)
        self.__writePackage(
            bytearray(
                [0xFF, 0x55, 0x04, self._clamp_byte(extID), 0x01, 0x03, self._clamp_byte(port)]
            )
        )

    def requestButtonOnBoard(self, extID, callback):
        self.__doCallback(extID, callback)
        self.__writePackage(
            bytearray([0xFF, 0x55, 0x04, self._clamp_byte(extID), 0x01, 0x1F, 0x07])
        )

    def requestIROnBoard(self, extID, callback):
        self.__doCallback(extID, callback)
        self.__writePackage(bytearray([0xFF, 0x55, 0x03, self._clamp_byte(extID), 0x01, 0x0D]))

    def requestUltrasonicSensor(self, extID, port, callback):
        self.__doCallback(extID, callback)
        self.__writePackage(
            bytearray(
                [0xFF, 0x55, 0x04, self._clamp_byte(extID), 0x01, 0x01, self._clamp_byte(port)]
            )
        )

    def requestLineFollower(self, extID, port, callback):
        self.__doCallback(extID, callback)
        self.__writePackage(
            bytearray(
                [0xFF, 0x55, 0x04, self._clamp_byte(extID), 0x01, 0x11, self._clamp_byte(port)]
            )
        )

    # -------------------------------------------------------------------------
    # Cadet Engineer / Kid-Friendly Pythonic API
    # -------------------------------------------------------------------------

    def rgb_led(self, port, slot, *args):
        """Set RGB LED color.

        Supports both 5-argument Cadet syntax:
            rover.rgb_led(port, slot, red, green, blue)
        and 6-argument explicit index syntax:
            rover.rgb_led(port, slot, index, red, green, blue)

        When port == 0, targets the original mBot (mCore) onboard RGB LEDs
        (hardware port 7, slot 2), using `slot` as the LED index (0=both, 1=left, 2=right).
        """
        if len(args) == 3:
            red, green, blue = args
            if port == 0:
                self.doRGBLed(0x07, 0x02, slot, red, green, blue)
            else:
                self.doRGBLed(port, slot if slot > 0 else 2, 0, red, green, blue)
        elif len(args) == 4:
            index, red, green, blue = args
            hw_port = 0x07 if port == 0 else port
            hw_slot = 0x02 if (port == 0 and slot == 0) else slot
            self.doRGBLed(hw_port, hw_slot, index, red, green, blue)
        else:
            raise TypeError(
                "rgb_led() expects (port, slot, red, green, blue) "
                "or (port, slot, index, red, green, blue)"
            )

    def set_color(self, red, green, blue, index=0):
        """Set onboard RGB LED color (index: 0=both, 1=LED1, 2=LED2)."""
        self.doRGBLedOnBoard(index, red, green, blue)

    def buzzer(self, frequency_hz, duration_ms=0):
        """Broadcast a tone on the onboard piezo buzzer."""
        self.doBuzzer(frequency_hz, duration_ms)

    def play_tone(self, frequency_hz, duration_ms=500):
        """Alias for buzzer() with a 500ms default duration."""
        self.doBuzzer(frequency_hz, duration_ms)

    def move(self, left_speed, right_speed):
        """Drive left and right motors (-255 to 255)."""
        self.doMove(left_speed, right_speed)

    def forward(self, speed=100, duration=None):
        """Drive forward at `speed`, optionally stopping after `duration` seconds."""
        self.doMove(speed, speed)
        if duration is not None:
            sleep(duration)
            self.stop()

    def backward(self, speed=100, duration=None):
        """Drive backward at `speed`, optionally stopping after `duration` seconds."""
        self.doMove(-speed, -speed)
        if duration is not None:
            sleep(duration)
            self.stop()

    def turn_left(self, speed=100, duration=None):
        """Pivot left at `speed`, optionally stopping after `duration` seconds."""
        self.doMove(-speed, speed)
        if duration is not None:
            sleep(duration)
            self.stop()

    def turn_right(self, speed=100, duration=None):
        """Pivot right at `speed`, optionally stopping after `duration` seconds."""
        self.doMove(speed, -speed)
        if duration is not None:
            sleep(duration)
            self.stop()

    def stop(self):
        """Halt both drive motors."""
        self.command_log.append({"action": "stop", "left": 0, "right": 0})
        self.doMove(0, 0)

    def _sync_request(self, dispatch_fn, timeout=1.0, default=None):
        with self._lock:
            ext_id = self._next_ext_id
            self._next_ext_id = 80 if self._next_ext_id >= 250 else self._next_ext_id + 1
            event = threading.Event()
            self._sync_events[ext_id] = event

        def _on_response(val):
            self._sync_results[ext_id] = val
            event.set()

        dispatch_fn(ext_id, _on_response)
        received = event.wait(timeout=timeout)
        with self._lock:
            self._sync_events.pop(ext_id, None)
            return self._sync_results.pop(ext_id, default) if received else default

    def get_distance(self, port=3, timeout=1.0):
        """Synchronously read ultrasonic distance in cm on `port` (default port 3)."""
        return self._sync_request(
            lambda ext_id, cb: self.requestUltrasonicSensor(ext_id, port, cb),
            timeout=timeout,
            default=0.0,
        )

    ultrasonic = get_distance

    def get_light(self, port=8, timeout=1.0):
        """Synchronously read light sensor level (0-1023) on `port` (default onboard port 8)."""
        return self._sync_request(
            lambda ext_id, cb: self.requestLight(ext_id, port, cb),
            timeout=timeout,
            default=0.0,
        )

    light_sensor = get_light

    def get_line_follower(self, port=2, timeout=1.0):
        """Synchronously read line follower state (0-3) on `port` (default port 2)."""
        return self._sync_request(
            lambda ext_id, cb: self.requestLineFollower(ext_id, port, cb),
            timeout=timeout,
            default=0.0,
        )

    line_follower = get_line_follower

    def is_button_pressed(self, timeout=1.0):
        """Synchronously read onboard button state as a boolean."""
        val = self._sync_request(
            lambda ext_id, cb: self.requestButtonOnBoard(ext_id, cb),
            timeout=timeout,
            default=0,
        )
        return bool(val)

    button_pressed = is_button_pressed

    # -------------------------------------------------------------------------
    # Frame Parser & Binary Helpers
    # -------------------------------------------------------------------------

    def onParse(self, byte):
        value = 0
        self.buffer.append(int(byte) & 0xFF)
        bufferLength = len(self.buffer)
        if bufferLength >= 2:
            if self.buffer[bufferLength - 1] == 0x55 and self.buffer[bufferLength - 2] == 0xFF:
                self.isParseStart = True
                self.isParseStartIndex = bufferLength - 2
            if (
                self.buffer[bufferLength - 1] == 0x0A
                and self.buffer[bufferLength - 2] == 0x0D
                and self.isParseStart
            ):
                self.isParseStart = False
                # Ignore empty ACK frames (0xFF 0x55 0x0D 0x0A)
                if bufferLength - self.isParseStartIndex < 6:
                    self.buffer = []
                    return
                position = self.isParseStartIndex + 2
                extID = self.buffer[position]
                position += 1
                data_type = self.buffer[position]
                position += 1
                # 1: byte, 2: float, 3: short, 4: len+string, 5: double
                if data_type == 1:
                    value = self.buffer[position]
                elif data_type == 2:
                    value = self.readFloat(position)
                    if value < -255 or value > 1023:
                        value = 0
                elif data_type == 3:
                    value = self.readShort(position)
                elif data_type == 4:
                    value = self.readString(position)
                elif data_type == 5:
                    value = self.readDouble(position)
                if 1 <= data_type <= 5:
                    self.responseValue(extID, value)
                self.buffer = []

    def readFloat(self, position):
        v = self.buffer[position : position + 4]
        if len(v) < 4:
            return 0.0
        return struct.unpack("<f", bytes(v))[0]

    def readShort(self, position):
        v = self.buffer[position : position + 2]
        if len(v) < 2:
            return 0
        return struct.unpack("<h", bytes(v))[0]

    def readString(self, position):
        if position >= len(self.buffer):
            return ""
        length = self.buffer[position]
        position += 1
        raw = bytes(self.buffer[position : position + length])
        return raw.decode("utf-8", errors="replace")

    def readDouble(self, position):
        v = self.buffer[position : position + 4]
        if len(v) < 4:
            return 0.0
        return struct.unpack("<f", bytes(v))[0]

    def responseValue(self, extID, value):
        callback = self.__selectors.get("callback_" + str(extID))
        if callback is not None:
            callback(value)

    def __doCallback(self, extID, callback):
        self.__selectors["callback_" + str(extID)] = callback

    def float2bytes(self, fval):
        return list(struct.pack("<f", float(fval)))

    def short2bytes(self, sval):
        return list(struct.pack("<h", int(sval)))


class mbot(mBot):
    """Auto-connecting Rover interface used in Cadet Engineer missions (`rover = mbot()`)."""

    def __init__(self, port=None, use_hid=False, auto_connect=True, simulate=None):
        super().__init__(
            auto_connect=auto_connect,
            port=port,
            use_hid=use_hid,
            simulate=simulate,
        )
