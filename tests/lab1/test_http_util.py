import io
from src.util.http_util import *

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

