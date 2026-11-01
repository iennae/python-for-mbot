"""Backward-compatible shim so legacy `from lib.mBot import *` scripts continue to work."""

from mbot.mBot import mBot, mbot, mHID, mLoopback, mSerial, sleep

__all__ = ["mBot", "mHID", "mLoopback", "mSerial", "mbot", "sleep"]
