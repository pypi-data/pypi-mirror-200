#  Copyright (c) ETH Zurich, SIS ID and HVL D-ITET
#
"""Devices subpackage."""

import sys

from .base import (  # noqa: F401
    Device,
    DeviceError,
    DeviceExistingError,
    DeviceFailuresError,
    DeviceSequenceMixin,
    SingleCommDevice,
)
from .crylas import (  # noqa: F401
    CryLasAttenuator,
    CryLasAttenuatorConfig,
    CryLasAttenuatorError,
    CryLasAttenuatorSerialCommunication,
    CryLasAttenuatorSerialCommunicationConfig,
    CryLasLaser,
    CryLasLaserConfig,
    CryLasLaserError,
    CryLasLaserNotReadyError,
    CryLasLaserSerialCommunication,
    CryLasLaserSerialCommunicationConfig,
)
from .ea_psi9000 import (  # noqa: F401
    PSI9000,
    PSI9000Config,
    PSI9000Error,
    PSI9000VisaCommunication,
    PSI9000VisaCommunicationConfig,
)
from .fug import (  # noqa: F401
    FuG,
    FuGConfig,
    FuGDigitalVal,
    FuGError,
    FuGErrorcodes,
    FuGMonitorModes,
    FuGPolarities,
    FuGRampModes,
    FuGReadbackChannels,
    FuGSerialCommunication,
    FuGSerialCommunicationConfig,
    FuGTerminators,
)
from .heinzinger import (  # noqa: F401
    HeinzingerConfig,
    HeinzingerDI,
    HeinzingerPNC,
    HeinzingerPNCDeviceNotRecognizedError,
    HeinzingerPNCError,
    HeinzingerPNCMaxCurrentExceededError,
    HeinzingerPNCMaxVoltageExceededError,
    HeinzingerSerialCommunication,
    HeinzingerSerialCommunicationConfig,
)

try:
    from .labjack import LabJack, LabJackError, LabJackIdentifierDIOError  # noqa: F401
except (ImportError, ModuleNotFoundError):
    import warnings

    warnings.warn(
        "\n\n  "
        "To use LabJack device controller or related utilities install LJM Library and"
        "\n  "
        "install the hvl_ccb library with a 'labjack' extra feature:"
        "\n\n  "
        "    pip install hvl_ccb[labjack]"
        "\n\n"
    )

from .lauda import (  # noqa: F401
    LaudaProRp245e,
    LaudaProRp245eConfig,
    LaudaProRp245eTcpCommunication,
    LaudaProRp245eTcpCommunicationConfig,
)
from .mbw973 import (  # noqa: F401
    MBW973,
    MBW973Config,
    MBW973ControlRunningError,
    MBW973Error,
    MBW973PumpRunningError,
    MBW973SerialCommunication,
    MBW973SerialCommunicationConfig,
)
from .newport import (  # noqa: F401
    NewportConfigCommands,
    NewportControllerError,
    NewportMotorError,
    NewportMotorPowerSupplyWasCutError,
    NewportSerialCommunicationError,
    NewportSMC100PP,
    NewportSMC100PPConfig,
    NewportSMC100PPSerialCommunication,
    NewportSMC100PPSerialCommunicationConfig,
    NewportStates,
    NewportUncertainPositionError,
)
from .pfeiffer_tpg import (  # noqa: F401
    PfeifferTPG,
    PfeifferTPGConfig,
    PfeifferTPGError,
    PfeifferTPGSerialCommunication,
    PfeifferTPGSerialCommunicationConfig,
)

if sys.platform == "darwin":
    import warnings

    warnings.warn("\n\n  PicoSDK is not available for Darwin OSs\n")
else:
    try:
        from .picotech_pt104 import (  # noqa: F401
            Pt104,
            Pt104ChannelConfig,
            Pt104CommunicationType,
            Pt104DeviceConfig,
        )
    except (ImportError, ModuleNotFoundError):
        import warnings

        warnings.warn(
            "\n\n  "
            "To use PicoTech PT-104 device controller or related utilities install"
            "\n  "
            "PicoSDK and install the hvl_ccb library with a 'picotech' extra feature:"
            "\n\n  "
            "    $ pip install hvl_ccb[picotech]"
            "\n\n"
        )

from .rs_rto1024 import (  # noqa: F401
    RTO1024,
    RTO1024Config,
    RTO1024Error,
    RTO1024VisaCommunication,
    RTO1024VisaCommunicationConfig,
)
from .se_ils2t import (  # noqa: F401
    ILS2T,
    ILS2TConfig,
    ILS2TError,
    ILS2TModbusTcpCommunication,
    ILS2TModbusTcpCommunicationConfig,
    IoScanningModeValueError,
    ScalingFactorValueError,
)
from .sst_luminox import (  # noqa: F401
    Luminox,
    LuminoxConfig,
    LuminoxMeasurementType,
    LuminoxMeasurementTypeError,
    LuminoxOutputMode,
    LuminoxOutputModeError,
    LuminoxSerialCommunication,
    LuminoxSerialCommunicationConfig,
)
from .visa import VisaDevice, VisaDeviceConfig  # noqa: F401
