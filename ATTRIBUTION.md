# Attribution & Original Project Context

This repository (`iennae/python-for-mbot`) is a modernized fork of [`xeecos/python-for-mbot`](https://github.com/xeecos/python-for-mbot), originally created as a Python 2.7 interface for the Makeblock mBot.

The notes below are preserved from the original upstream repository to retain historical context and author credit.

---

## Fork Additions (`iennae/python-for-mbot`)

Newly created files in this fork (including the `missions/` curriculum and starter templates, `site/` Mission Control web application, `scripts/build_site.py`, `tests/`, and `.github/workflows/`) are **Copyright 2026 Jennifer Davis** and licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). Original upstream files originating from [`xeecos/python-for-mbot`](https://github.com/xeecos/python-for-mbot) retain their upstream license ([`LICENSE`](LICENSE)).

---

## Original Upstream Description (`xeecos/python-for-mbot`)

A Python interface to control and communicate with mBot robot kit from Makeblock.

This has been tested with:
* the Raspberry PI.
* the Intel Edison.

It works on Linux, Windows 7/10 and OS X.

---

## Classic Callback API Usage (`examples/`)

The original callback-driven API (`from lib.mBot import *`) is preserved via the `src/lib/` compatibility shim, and the original example scripts are located in [`examples/`](examples/):

```python
from lib.mBot import *


def onLight(value):
    print("light = ", value)


if __name__ == "__main__":
    bot = mBot()
    bot.startWithSerial()  # Auto-detects USB serial port (or pass e.g. "COM15" / "/dev/ttyUSB0")
    try:
        while True:
            bot.requestLightOnBoard(1, onLight)
            sleep(0.5)
    except KeyboardInterrupt:
        bot.close()
```

Using wireless HID (requires `pip install -e ".[hid]"`):
```python
bot.startWithHID()
```
