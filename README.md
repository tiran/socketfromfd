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
