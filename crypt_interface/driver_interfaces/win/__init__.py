"""
Initial inspiration for CreateFile and DeviceIOControl interfacing from:
    https://gist.github.com/santa4nt/11068180
"""

from crypt_interface.driver_interfaces.win import (
    win_constants, base_win_models, base_win_driver_models)

__all__ = [win_constants, base_win_models, base_win_driver_models]
