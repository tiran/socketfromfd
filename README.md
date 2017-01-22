# socketfromfd -- Create a socket from a file descriptor

socketfromfd is an enhanced version of
[socket.fromfd()](https://docs.python.org/3/library/socket.html#socket.fromfd)
from Python's standard library. It uses ctypes and libc's [getsockopt()](http://linux.die.net/man/2/getsockopt)
function to auto-detect the file descriptor's socket family, type and protocol.

```python
>>> import socket
>>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>>> sock
<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 0)>

>>> from socketfromfd import fromfd
>>> newsock = fromfd(sock.fileno())
>>> newsock
<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6, laddr=('0.0.0.0', 0)>
```

The parameter ``keep_fd``` lets you re-use the original fd under Python 3.
Because Python 2 always duplicated the fd, it is not possible to provide
the same behavior with Python 2. Instead ```keep_fd=False``` simply closes
the input fd.

```python
>>> newsock = fromfd(sock.fileno(), keep_fd=False)
>>> newsock
<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6, laddr=('0.0.0.0', 0)>
```

## What's wrong with the Python standard library?

Python assumes ```AF_INET``` (aka IPv4) as default. It breaks even this
simple example in multiple ways. For one ```getpeername``` returns something
that is neither a valid IPv4 nor a valid IPv6 address. For ``AF_INET```
the method ```getpeername``` is suppose to return a tuple of two elements,
not four elements, too.

```python
>>> import socket
>>> sock = socket.create_connection(('www.python.org', 443))
>>> sock.family
<AddressFamily.AF_INET6: 10>
>>> sock.getpeername()
('2a04:4e42:1b::223', 443, 0, 0)

>>> newsock = socket.socket(fileno=sock.fileno())
>>> newsock.family
<AddressFamily.AF_INET: 2>
>>> newsock.getpeername()
('2a04:4e42:1b:0:4890:7147:307f:0%1197553104', 443, 0, 1197553104)

>>> socket.gethostbyname('www.python.org')
'151.101.112.223'
>>> sock4 = socket.create_connection(('151.101.112.223', 443))
>>> sock4.getpeername()
('151.101.112.223', 443)
```

https://bugs.python.org/issue28134
