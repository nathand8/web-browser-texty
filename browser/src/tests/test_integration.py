from src.util.url_util import *
from src.util.socket_util import *

def test_socket_example_org():
    protocol, host, port, path = splitURL("http://example.org/index.html")
    es = EnhancedSocket()
    es.connect(host, port)
    es.sendLines(["GET /index.html HTTP/1.0", "Host: example.org"])
    response = es.makefile()

    # Status Line
    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)

    # Headers
    headers = {}
    while True:
        line = response.readline()
        if line == SOCKET_NEWLINE: break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()

    for k, v in headers.items():
        print(k, ":", v)