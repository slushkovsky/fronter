#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 16:19:08 2016

@author: chernov
"""

from os import environ, path

def __add_lib_path():
    lib_path = path.abspath(path.dirname(__file__))
    ld_lib_path = ""
    if "LD_LIBRARY_PATH" in environ:
        ld_lib_path = environ["LD_LIBRARY_PATH"]
        lib_paths = ld_lib_path.split(":")
        if lib_path in lib_paths:
            return
    environ["LD_LIBRARY_PATH"] = "%s:%s"%(ld_lib_path, lib_path)
    
    
__add_lib_path()

from tess_c_api import *
