import os
import re
from enum import Enum
from argparse import ArgumentError
from geomtypes import Size


def size(value): 
    m = re.match('(?P<width>\d+)x(?P<height>\d+)', value.strip())
    
    if not m:
        raise ArgumentError('Size not supported: {!r} (format: WxH)')            
    
    return Size(int(m.group('width')), int(m.group('height')))

def existed_dir(value): 
    return __existed_path_arg(value, __PathType.DIR)

def existed_file(value): 
    return __existed_path_arg(value, __PathType.FILE)


class __PathType(Enum): 
    DIR     = 'directory'
    FILE    = 'file'
    LINK    = 'link'
    MOUNT   = 'mount'
    UNKNOWN = 'unknown'


def __existed_path_arg(path, type): 
    ''' 
      Processes path: checks existance and type, changes to relative form  

      @param  path  <str>               Path
      @param  type  <str (__PathType)>  Required type 

      @return  <str>  relative form of @param(path)
    '''

    assert(isinstance(path, str))
    assert(type in __PathType)

    if not os.path.exists(path): 
        raise ArgumentError('Path {path!r} is not exists'.format(path=path))

    path_type = __path_type(path)

    if path_type != type: 
        tmpl = '{path!r} type is {type!r} istead of {need!r}'
        raise ArgumentError(tmpl.format(path=path, type=path_type, need=type))

    return os.path.realpath(path)


def __path_type(path):
    '''
      Determines path type (one of types, listed in __PathType enum)

      @param  path  <str>  Existed path (if path is not exists - wil be raised AssertionError)

      @return  <str>  __PathType element  
    '''

    assert(isinstance(path, str)) 
    assert(os.path.exists(path))

    return __PathType.DIR   if os.path.isdir  (path) else \
           __PathType.FILE  if os.path.isfile (path) else \
           __PathType.LINK  if os.path.islink (path) else \
           __PathType.MOUNT if os.path.ismount(path) else \
           __PathType.UNKNOWN