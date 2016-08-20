# Copyright (C) 2016  Christian Heimes
"""socketfromfd -- socket.fromd() with auto-discovery
"""
from __future__ import print_function

import ctypes
import os
import socket
from ctypes.util import find_library

__all__ = ('fromfd',)

SO_DOMAIN = getattr(socket, 'SO_DOMAIN', 39)
SO_TYPE = getattr(socket, 'SO_TYPE', 3)
SO_PROTOCOL = getattr(socket, 'SO_PROTOCOL', 38)


_libc_name = find_library('c')
if _libc_name is not None:
    libc = ctypes.CDLL(_libc_name, use_errno=True)
else:
    raise OSError('libc not found')


def _errcheck_errno(result, func, arguments):
    """Raise OSError by errno for -1
    """
    if result == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return arguments


_libc_getsockopt = libc.getsockopt
_libc_getsockopt.argtypes = [
    ctypes.c_int,  # int sockfd
    ctypes.c_int,  # int level
    ctypes.c_int,  # int optname
    ctypes.c_void_p,  # void *optval
    ctypes.POINTER(ctypes.c_uint32)  # socklen_t *optlen
]
_libc_getsockopt.restype = ctypes.c_int  # 0: ok, -1: err
_libc_getsockopt.errcheck = _errcheck_errno


def _raw_getsockopt(fd, level, optname):
    """Make raw getsockopt() call for int32 optval

    :param fd: socket fd
    :param level: SOL_*
    :param optname: SO_*
    :return: value as int
    """
    optval = ctypes.c_int(0)
    optlen = ctypes.c_uint32(4)
    _libc_getsockopt(fd, level, optname,
                     ctypes.byref(optval), ctypes.byref(optlen))
    return optval.value


def fromfd(fd):
    """Create a socket from a file descriptor

    socket domain (family), type and protocol are auto-detected. The socket
    uses a dup()ed fd. The original fd can be closed.

    :param fd: socket fd
    :return: socket.socket instance
    :raises OSError: for invalid socket fd
    """
    family = _raw_getsockopt(fd, socket.SOL_SOCKET, SO_DOMAIN)
    typ = _raw_getsockopt(fd, socket.SOL_SOCKET, SO_TYPE)
    proto = _raw_getsockopt(fd, socket.SOL_SOCKET, SO_PROTOCOL)
    sock = socket.fromfd(fd, family, typ, proto)
    return sock
