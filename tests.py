# Copyright (C) 2016  Christian Heimes

import errno
import socket
import sys
import unittest

from socketfromfd import fromfd, _raw_getsockopt
from socketfromfd import SO_DOMAIN, SO_PROTOCOL, SO_TYPE

PROTO_TCP = socket.getprotobyname('tcp')
PROTO_UDP = socket.getprotobyname('udp')


def try_close(sock):
    """Close socket and ignore bad file descriptor

    Python 3.6 raises "OSError: [Errno 9] Bad file descriptor" when the
    fd has already been closed.
    """
    try:
        sock.close()
    except OSError as e:
        if e.errno != errno.EBADF:
            raise


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
            self.assertIsInstance(newsock, socket.socket)
        finally:
            newsock.close()

        newsock = fromfd(sock.fileno(), keep_fd=False)
        try:
            if sys.version_info.major >= 3:
                self.assertEqual(sock.fileno(), newsock.fileno())
            else:
                self.assertNotEqual(sock.fileno(), newsock.fileno())
            self.assertEqual(newsock.family, sock.family)
            self.assertEqual(newsock.type, sock.type)
            self.assertEqual(newsock.proto, sock.proto)
            self.assertIsInstance(newsock, socket.socket)
        finally:
            newsock.close()

    def _test_socket(self, family, typ, proto):
        sock = socket.socket(family, typ, proto)
        try:
            self.assert_socket(sock)
        finally:
            try_close(sock)

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

    def _test_fromfd_network(self, keep_fd):
        sock = socket.create_connection(('www.pythontest.net', 80))
        newsock = None
        try:
            self.assertIn(sock.family, (socket.AF_INET, socket.AF_INET6))
            self.assertEqual(sock.type, socket.SOCK_STREAM)
            newsock = fromfd(sock.fileno(), keep_fd)
            if keep_fd:
                self.assertNotEqual(sock.fileno(), newsock.fileno())
            elif sys.version_info.major >= 3:
                self.assertEqual(sock.fileno(), newsock.fileno())
            newsock.sendall(b'GET / HTTP/1.1\r\n\r\n')
            newsock.recv(1024)
        finally:
            sock.close()
            if newsock:
                try_close(newsock)

    def test_fromfd_keep_fd(self):
        self._test_fromfd_network(True)
        self._test_fromfd_network(False)


if __name__ == '__main__':
    unittest.main()
