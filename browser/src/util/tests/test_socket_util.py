from src.util.socket_util import *

def test_connect(mocker):
    mocker.patch("socket.socket.connect")
    es = EnhancedSocket()
    es.connect("example.org", 80)
    socket.socket.connect.assert_called_once_with(("example.org", 80))

def test_sendLines(mocker):
    mocker.patch("socket.socket.send")
    es = EnhancedSocket()
    es.sendLines(["first", "second"])
    socket.socket.send.assert_called_once_with(b"first\r\nsecond\r\n\r\n")
