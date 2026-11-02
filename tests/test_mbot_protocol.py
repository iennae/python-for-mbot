# Copyright 2026 Jennifer Davis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct

import pytest

from mbot import mBot, mbot, mLoopback


def make_simulated_bot() -> mBot:
    bot = mBot(auto_connect=True, simulate=True)
    assert isinstance(bot.device, mLoopback)
    return bot


def test_short2bytes_and_float2bytes_python3() -> None:
    bot = mBot()
    assert bot.short2bytes(100) == [100, 0]
    assert bot.short2bytes(-100) == list(struct.pack("<h", -100))
    assert bot.short2bytes(440) == list(struct.pack("<h", 440))
    assert bot.float2bytes(12.5) == list(struct.pack("<f", 12.5))


def test_mission_01_rgb_led_and_buzzer_packets() -> None:
    """Verify exact wire bytes for Mission 01 calls (`rgb_led` and `buzzer`)."""
    rover = mbot(simulate=True)
    try:
        # Phase 1: rover.rgb_led(0, 0, 0, 255, 0) -> onboard port 7, slot 2, index 0
        rover.rgb_led(0, 0, 0, 255, 0)
        assert rover.device.sent_packages[-1] == bytearray(
            [0xFF, 0x55, 0x09, 0x00, 0x02, 0x08, 0x07, 0x02, 0x00, 0, 255, 0]
        )

        # Single onboard LED #1: rover.rgb_led(0, 1, 255, 0, 0) -> port 7, slot 2, index 1
        rover.rgb_led(0, 1, 255, 0, 0)
        assert rover.device.sent_packages[-1] == bytearray(
            [0xFF, 0x55, 0x09, 0x00, 0x02, 0x08, 0x07, 0x02, 0x01, 255, 0, 0]
        )

        # Phase 2: rover.buzzer(440, 300)
        rover.buzzer(440, 300)
        expected_buzzer = (
            bytearray([0xFF, 0x55, 0x07, 0x00, 0x02, 0x22])
            + bytearray(struct.pack("<h", 440))
            + bytearray(struct.pack("<h", 300))
        )
        assert rover.device.sent_packages[-1] == expected_buzzer

        # Phase 3: extinguish LEDs
        rover.rgb_led(0, 0, 0, 0, 0)
        assert rover.device.sent_packages[-1] == bytearray(
            [0xFF, 0x55, 0x09, 0x00, 0x02, 0x08, 0x07, 0x02, 0x00, 0, 0, 0]
        )
    finally:
        rover.close()


def test_motor_move_servo_sevseg_and_ir_packets() -> None:
    bot = make_simulated_bot()
    try:
        bot.doMove(100, -100)
        expected_move = (
            bytearray([0xFF, 0x55, 0x07, 0x00, 0x02, 0x05])
            + bytearray(struct.pack("<h", -100))
            + bytearray(struct.pack("<h", -100))
        )
        assert bot.device.sent_packages[-1] == expected_move

        bot.doMotor(9, 150)
        expected_motor = bytearray([0xFF, 0x55, 0x06, 0x00, 0x02, 0x0A, 9]) + bytearray(
            struct.pack("<h", 150)
        )
        assert bot.device.sent_packages[-1] == expected_motor

        bot.doServo(1, 2, 90)
        assert bot.device.sent_packages[-1] == bytearray(
            [0xFF, 0x55, 0x06, 0x00, 0x02, 0x0B, 1, 2, 90]
        )

        bot.doSevSegDisplay(1, 3.5)
        expected_sevseg = bytearray([0xFF, 0x55, 0x08, 0x00, 0x02, 0x09, 1]) + bytearray(
            struct.pack("<f", 3.5)
        )
        assert bot.device.sent_packages[-1] == expected_sevseg

        bot.doIROnBoard("SOS")
        assert bot.device.sent_packages[-1] == bytearray(
            [0xFF, 0x55, 6, 0x00, 0x02, 0x0D, ord("S"), ord("O"), ord("S")]
        )
    finally:
        bot.close()


def test_on_parse_sensor_responses_and_ack() -> None:
    bot = mBot()
    received = {}

    # 1. Empty callOK() ACK frame (0xFF 0x55 0x0D 0x0A) should be ignored cleanly
    for b in [0xFF, 0x55, 0x0D, 0x0A]:
        bot.onParse(b)
    assert bot.buffer == []

    # 2. Float sensor response (type 2): ultrasonic 37.5 cm on extID 1
    bot.requestUltrasonicSensor(1, 3, lambda val: received.setdefault("ultrasonic", val))
    float_bytes = list(struct.pack("<f", 37.5))
    for b in [0xFF, 0x55, 1, 2, *float_bytes, 0x0D, 0x0A]:
        bot.onParse(b)
    assert pytest.approx(received["ultrasonic"], rel=1e-5) == 37.5

    # 3. Byte sensor response (type 1): button pressed = 1 on extID 2
    bot.requestButtonOnBoard(2, lambda val: received.setdefault("button", val))
    for b in [0xFF, 0x55, 2, 1, 1, 0x0D, 0x0A]:
        bot.onParse(b)
    assert received["button"] == 1

    # 4. Short sensor response (type 3): -120 on extID 3
    bot._mBot__doCallback(3, lambda val: received.setdefault("short", val))
    short_bytes = list(struct.pack("<h", -120))
    for b in [0xFF, 0x55, 3, 3, *short_bytes, 0x0D, 0x0A]:
        bot.onParse(b)
    assert received["short"] == -120

    # 5. String response (type 4): firmware version "06.01.107" on extID 4
    bot._mBot__doCallback(4, lambda val: received.setdefault("version", val))
    ver = b"06.01.107"
    for b in [0xFF, 0x55, 4, 4, len(ver), *ver, 0x0D, 0x0A]:
        bot.onParse(b)
    assert received["version"] == "06.01.107"


def test_synchronous_sensor_queries_in_simulation() -> None:
    with mbot(simulate=True) as rover:
        assert pytest.approx(rover.get_distance(), rel=1e-5) == 42.0
        assert pytest.approx(rover.get_light(), rel=1e-5) == 42.0
        assert pytest.approx(rover.get_line_follower(), rel=1e-5) == 42.0
        assert rover.is_button_pressed() is False
