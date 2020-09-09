from src.util.socket_util import *
import tkinter
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


def request(url):
    scheme, host, port, path = splitURL(url)
    encrypted = scheme == "https"
    es = EnhancedSocket()
    es.connect(host, port, encrypted=encrypted)
    es.sendLines([
        "GET {} HTTP/1.1".format(path),
        "Host: {}".format(host),
        "User-Agent: CS-6968-UofU",
        "Connection: close"
    ])
    response = es.makefile()
    status, headers, html = parseHTTPResponse(response)
    es.close()
    assert status == "200", "{}: {}".format(status, explanation)
    return headers, html

# Get the body out of the html
# If no body match is found, return all the html
def getBody(html):
    bodyRegex = r'<\s*body.*?>([\s\S]*)<\s*\/body\s?>'
    bodyRegexMatch = re.search(bodyRegex, html, flags=re.MULTILINE)
    if not bodyRegexMatch:
        return html
    return bodyRegexMatch.group()

def show(html):
    print(stripTags(html))

def lex(body):
    return stripTags(body)


# Constants for the layout
WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 40

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.display_list = []
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
    
    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        print("scroll down", self.scroll)
        self.render()
    
    def layout(self, text):
        self.display_list = []
        x, y = HSTEP, VSTEP
        for c in text.strip():
            self.display_list.append((x, y, c))
            x += HSTEP
            if x >= WIDTH - HSTEP:
                y += VSTEP
                x = HSTEP
        self.render()
    
    def render(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)


if __name__ == "__main__":
    import sys
    headers, html = request(sys.argv[1])
    displayText = lex(getBody(html))
    show(displayText)

    browser = Browser()
    browser.layout(displayText)
    tkinter.mainloop()
