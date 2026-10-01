from pkg.core import stamp


def test_stamp_is_recent() -> None:
    assert stamp().year >= 2020


def test_fetch() -> None:
    import socket

    socket.getaddrinfo("example.com", 80)
