#  Copyright (c) ETH Zurich, SIS ID and HVL D-ITET
#
"""
Constants, Heinzinger Digital Interface I/II and Heinzinger PNC power supply.
Descriptors for errors
"""

import logging

from hvl_ccb.dev.base import DeviceError

logger = logging.getLogger(__name__)


class HeinzingerPNCError(DeviceError):
    """
    General error with the Heinzinger PNC voltage source.
    """

    pass


class HeinzingerPNCMaxVoltageExceededError(HeinzingerPNCError):
    """
    Error indicating that program attempted to set the voltage
    to a value exceeding 'max_voltage'.
    """

    pass


class HeinzingerPNCMaxCurrentExceededError(HeinzingerPNCError):
    """
    Error indicating that program attempted to set the current
    to a value exceeding 'max_current'.
    """

    pass


class HeinzingerPNCDeviceNotRecognizedError(HeinzingerPNCError):
    """
    Error indicating that the serial number of the device
    is not recognized.
    """

    pass
