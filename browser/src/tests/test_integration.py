from src.util.url_util import *
from src.util.socket_util import *
from src.util.http_util import *

def test_socket_example_org():
    protocol, host, port, path = splitURL("http://example.org/index.html")
    es = EnhancedSocket()
    es.connect(host, port)
    es.sendLines(["GET /index.html HTTP/1.0", "Host: example.org"])
    response = es.makefile()
    status, headers, html = parseHTTPResponse(response)
    es.close()
    assert status == "200"
    assert "content-type" in headers.keys()
    assert "This domain is for use in illustrative examples in documents." in html