from src.util.socket_util import *
from src.browser import *
from src.connection import *
from src.lexer import *
from src.layout import *

def test_example_org():
    scheme, host, port, path = splitURL("http://example.org/index.html")
    es = EnhancedSocket()
    es.connect(host, port)
    es.sendLines(["GET /index.html HTTP/1.0", "Host: example.org"])
    response = es.makefile()
    status, headers, html = parseHTTPResponse(response)
    es.close()
    assert status == "200"
    assert "content-type" in headers.keys()
    assert "This domain is for use in illustrative examples in documents." in html

def test_https_example_org():
    scheme, host, port, path = splitURL("https://example.org/index.html")
    assert scheme == "https"
    assert port == 443
    es = EnhancedSocket()
    es.connect(host, port, encrypted=True)
    es.sendLines(["GET /index.html HTTP/1.0", "Host: example.org"])
    response = es.makefile()
    status, headers, html = parseHTTPResponse(response)
    es.close()
    print(headers)
    assert status == "200"
    assert "content-type" in headers.keys()
    assert "This domain is for use in illustrative examples in documents." in html

def test_request_and_show():
    headers, html = request("https://browser.engineering/draft/graphics.html")
    assert "content-type" in headers.keys()
    assert "Drawing to the Screen" in html
    show(html)