from src.util.html_util import *
from src.util.url_util import *
from src.util.socket_util import *
from src.util.http_util import *

def request(url):
    scheme, host, port, path = splitURL(url)
    encrypted = scheme == "https"
    es = EnhancedSocket()
    es.connect(host, port, encrypted=encrypted)
    es.sendLines([
        "GET {} HTTP/1.0".format(path),
        "Host: {}".format(host)
    ])
    response = es.makefile()
    status, headers, html = parseHTTPResponse(response)
    es.close()
    assert status == "200", "{}: {}".format(status, explanation)
    return headers, html

def show(html):
    print(stripTags(html))

if __name__ == "__main__":
    import sys
    headers, html = request(sys.argv[1])
    show(html)
