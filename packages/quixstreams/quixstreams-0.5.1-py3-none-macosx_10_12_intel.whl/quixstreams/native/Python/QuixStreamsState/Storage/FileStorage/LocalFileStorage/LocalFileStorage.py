# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .....InteropHelpers.InteropUtils import InteropUtils


class LocalFileStorage(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type LocalFileStorage
        
        Returns
        ----------
        
        LocalFileStorage:
            Instance wrapping the .net type LocalFileStorage
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = LocalFileStorage._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(LocalFileStorage, cls).__new__(cls)
            LocalFileStorage._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type LocalFileStorage
        
        Returns
        ----------
        
        LocalFileStorage:
            Instance wrapping the .net type LocalFileStorage
        """
        if '_LocalFileStorage_pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self._pointer_owner = net_pointer
            self._pointer = net_pointer.get_interop_ptr__()
        else:
            self._pointer = net_pointer
        
        if finalize:
            self._finalizer = weakref.finalize(self, self._finalizerfunc)
            self._finalizer.atexit = False
        else:
            self._finalizer = lambda: None
    
    def _finalizerfunc(self):
        del LocalFileStorage._weakrefs[self._pointer.value]
        InteropUtils.free_hptr(self._pointer)
        self._finalizer.detach()
    
    def get_interop_ptr__(self) -> c_void_p:
        return self._pointer
    
    def dispose_ptr__(self):
        self._finalizer()
    
    def __enter__(self):
        pass
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._finalizer()
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("localfilestorage_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor(storageDirectory: str = None, autoCreateDir: bool = True) -> c_void_p:
        """
        Parameters
        ----------
        
        storageDirectory: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        autoCreateDir: bool
            (Optional) Underlying .Net type is Boolean. Defaults to True
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type LocalFileStorage
        """
        storageDirectory_ptr = InteropUtils.utf8_to_ptr(storageDirectory)
        autoCreateDir_bool = 1 if autoCreateDir else 0
        
        result = InteropUtils.invoke("localfilestorage_constructor", storageDirectory_ptr, autoCreateDir_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
