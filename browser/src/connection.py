from src.util.socket_util import *
import re

# This should take a url and split it into the scheme, host, and path
def splitURL(url):
    scheme, url = url.split("://", 1)
    assert scheme in ["http", "https"], "Unknown scheme: %s" % scheme
    host, path = url.split("/", 1)
    path = "/" + path
    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
    else:
        port = 80 if scheme == "http" else 443
    return scheme, host, port, path

# Return equivalent HTML with all tags removed
def stripTags(raw_html):
    html_sans_tags = ""
    in_angle = False
    for c in raw_html:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            html_sans_tags += c
    return html_sans_tags

# Parse the given response
# response: File
def parseHTTPResponse(response):

    # Status Line
    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    if status != "200":
        return status, {}, ""

    # Headers
    headers = {}
    while True:
        line = response.readline()
        if line == SOCKET_NEWLINE: break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()
    
    html = response.read()
    return status, headers, html
    
def request(url, payload=None):
    scheme, host, port, path = splitURL(url)
    method = "POST" if payload else "GET"
    encrypted = scheme == "https"
    es = EnhancedSocket()
    es.connect(host, port, encrypted=encrypted)
    lines = [
        "{} {} HTTP/1.1".format(method, path),
        "Host: {}".format(host),
        "User-Agent: CS-6968-UofU",
        "Connection: close",
    ]
    if payload:
        content_length = len(payload.encode("utf8"))
        lines += [
            "Content-Length: {}\r\n".format(content_length),
            "" + (payload or "")
        ]
    es.sendLines(lines)
    response = es.makefile()
    status, headers, html = parseHTTPResponse(response)
    es.close()
    assert status == "200", "{}: {}".format(status, explanation)
    return headers, html


# Get the body out of the html
# If no body match is found, return all the html
# DEPRECATED - Not Used Anymore
def getBody(html):
    bodyRegex = r'<\s*body.*?>([\s\S]*)<\s*\/body\s?>'
    bodyRegexMatch = re.search(bodyRegex, html, flags=re.MULTILINE)
    if not bodyRegexMatch:
        return html
    return bodyRegexMatch.group()

def show(html):
    print(stripTags(html))
