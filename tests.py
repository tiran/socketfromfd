# Copyright (C) 2016  Christian Heimes

import socket
import sys
import unittest

from socketfromfd import fromfd, _raw_getsockopt
from socketfromfd import SO_DOMAIN, SO_PROTOCOL, SO_TYPE

PROTO_TCP = socket.getprotobyname('tcp')
PROTO_UDP = socket.getprotobyname('udp')


class TestFromFD(unittest.TestCase):
    def assert_socket(self, sock):
        self.assertEqual(
            _raw_getsockopt(sock.fileno(), socket.SOL_SOCKET, SO_DOMAIN),
            sock.family
        )
        self.assertEqual(
            _raw_getsockopt(sock.fileno(), socket.SOL_SOCKET, SO_TYPE),
            sock.type
        )
        self.assertEqual(
            _raw_getsockopt(sock.fileno(), socket.SOL_SOCKET, SO_PROTOCOL),
            sock.proto
        )
        newsock = fromfd(sock.fileno())
        try:
            self.assertNotEqual(sock.fileno(), newsock.fileno())
            self.assertEqual(newsock.family, sock.family)
            self.assertEqual(newsock.type, sock.type)
            self.assertEqual(newsock.proto, sock.proto)
        finally:
            newsock.close()

    def _test_socket(self, family, typ, proto):
        sock = socket.socket(family, typ, proto)
        try:
            self.assert_socket(sock)
        finally:
            sock.close()

    def test_unix(self):
        self._test_socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        self._test_socket(socket.AF_UNIX, socket.SOCK_DGRAM, 0)
        self._test_socket(socket.AF_UNIX, socket.SOCK_SEQPACKET, 0)

    def test_ipv4(self):
        self._test_socket(socket.AF_INET, socket.SOCK_STREAM, PROTO_TCP)
        self._test_socket(socket.AF_INET, socket.SOCK_DGRAM, PROTO_UDP)

    def test_ipv6(self):
        self._test_socket(socket.AF_INET6, socket.SOCK_STREAM, PROTO_TCP)
        self._test_socket(socket.AF_INET6, socket.SOCK_DGRAM, PROTO_UDP)

    def test_error(self):
        with self.assertRaises(OSError):
            fromfd(sys.stdout.fileno())
        with self.assertRaises(OSError):
            fromfd(1000)


if __name__ == '__main__':
    unittest.main()
