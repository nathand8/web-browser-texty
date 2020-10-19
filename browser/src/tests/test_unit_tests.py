import io
import pytest
import mock

from src.browser import *
from src.connection import *
from src.lexer import *
from src.layout import *

# ========== Test splitURL ==========
def test_splitURL_example():
    scheme, host, port, path = splitURL("http://example.org/index.html")
    assert(scheme == "http")
    assert(host == "example.org")
    assert(port == 80) # Default port should be 80
    assert(path == "/index.html")

def test_splitURL_https():
    scheme, host, port, path = splitURL("https://example.org/index.html")
    assert(scheme == "https")
    assert(port == 443) # Encrypted port should be 80

def test_splitURL_custom_port():
    scheme, host, port, path = splitURL("http://example.org:8080/index.html")
    assert(scheme == "http")
    assert(host == "example.org")
    assert(port == 8080)
    assert(path == "/index.html")

def test_splitURL_custom_port_https():
    scheme, host, port, path = splitURL("https://example.org:8080/index.html")
    assert(scheme == "https")
    assert(host == "example.org")
    assert(port == 8080)
    assert(path == "/index.html")

def test_splitURL_empty_path():
    scheme, host, port, path = splitURL("http://example.org/")
    assert(path == "/")

def test_splitURL_bad_scheme():
    with pytest.raises(AssertionError) as error:
        splitURL("ftp://example.org/index.html")
    assert "Unknown scheme" in str(error.value)

# ========== Test parseHTTPResponse ==========
def test_parseHTTPResponse_example():
    test_response = """HTTP/1.0 200 OK
Accept-Ranges: bytes
Age: 190230

<!doctype html>
<html>
<head><title>Example Domain</title></head>
<body>
    <h1>Example Domain</h1>
    <p>This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission.</p>
    <p><a href="https://www.iana.org/domains/example">More information...</a></p>
</body>
</html>
    """
    # test_response = test_response.replace("\n", "\r\n")
    status, headers, html = parseHTTPResponse(io.StringIO(test_response, newline="\r\n"))
    assert status == "200"
    assert headers == {
        "accept-ranges": "bytes", # Headers should be lower-case keys
        "age": "190230"
    }
    assert html.startswith("<!doctype html>")
    assert "<html>" in html and "</html>" in html
    assert "<head>" in html and "</head>" in html
    assert "<body>" in html and "</body>" in html
    assert "This domain is for use in illustrative examples" in html and "</body>" in html

# ========== Test stripTags ==========
def test_stripTags_example():
    assert stripTags("<html><body>Hello</body></html>") == "Hello"
    assert stripTags("<!doctype html><script> something </script>") == " something "

# ========== Test getBody ===========
def test_getBody_example():
    assert getBody("<html><body>Some <div>elements</div> </body></html>") == "<body>Some <div>elements</div> </body>"

# ========= Test Browser.layout =========
# def test_browser_layout():
#     b = Browser()
#     b.width = 7
#     b.height = 20
#     b.hstep = 2
#     b.vstep = 3
#     b.layout("hello")
#     assert b.display_list == [
#         (2, 3, "h"), (4, 3, "e"),
#         (2, 6, "l"), (4, 6, "l"),
#         (2, 9, "o")
#     ]

# def test_browser_layout_strip_surrounding_whitespace():
#     b = Browser()
#     b.layout("\n\t \ra\n\t \r")
#     assert len(b.display_list) == 1

# def test_browser_layout_set_text():
#     b = Browser()
#     b.text = "unset"
#     b.layout("set")
#     assert b.text == "set"

# def test_browser_layout_set_text():
#     b = Browser()
#     b.text = "unset"
#     b.layout("set")
#     assert b.text == "set"

# def test_browser_window_resize():
#     b = Browser()
#     b.width = 0
#     b.height = 0
#     mockEvent = mock.Mock()
#     mockEvent.width = 10
#     mockEvent.height = 5
#     b.windowresize(mockEvent)
#     assert b.width == 10
#     assert b.height == 5

# def test_browser_scroll_down():
#     b = Browser()
#     b.scroll_step = 10
#     b.scroll = 2
#     b.scrolldown(None)
#     assert b.scroll == 12