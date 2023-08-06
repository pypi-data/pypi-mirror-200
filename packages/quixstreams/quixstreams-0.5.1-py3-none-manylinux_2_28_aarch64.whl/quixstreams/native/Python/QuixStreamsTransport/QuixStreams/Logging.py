# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...MicrosoftExtensionsLoggingAbstractions.Microsoft.Extensions.Logging.LogLevel import LogLevel
from ...InteropHelpers.InteropUtils import InteropUtils


class Logging(object):
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("logging_updatefactory")
    _interop_func.restype = None
    @staticmethod
    def UpdateFactory(logLevel: LogLevel) -> None:
        """
        Parameters
        ----------
        
        logLevel: LogLevel
            Underlying .Net type is LogLevel
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("logging_updatefactory", logLevel.value)
