from src.util.socket_util import *
import tkinter
import tkinter.font
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

class Text:
    def __init__(self, text):
        self.text = text

class Tag:
    def __init__(self, text):
        parts = text.split()
        self.tag = parts[0].lower()
        self.attributes = {}
        for attrpair in parts[1:]:
            if "=" in attrpair:
                key, value = attrpair.split("=", 1)
                if len(value) > 2 and value[0] in ["'", "\""]:
                    value = value[1:-1]
                self.attributes[key.lower()] = value
            else:
                self.attributes[attrpair.lower()] = ""
    
    def __repr__(self):
        return "<" + self.tag + " " + str(self.attributes) + ">"


def lex(body):
    # return stripTags(body)
    out = []
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if text: out.append(Text(text))
            text = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(text))
            text = ""
        else:
            text += c
    if not in_tag and text:
        out.append(Text(text))
    return out

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
        self.canvas.pack(expand=True, fill="both")
        self.display_list = []
        self.scroll = 0
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Configure>", self.windowresize)
        self.width = WIDTH
        self.height = HEIGHT
        self.hstep = HSTEP
        self.vstep = VSTEP
        self.scroll_step = SCROLL_STEP
        self.tokens = []

        # http://www.zggdwx.com/
    
    def scrollup(self, e):
        self.scroll -= self.scroll_step
        self.render()

    def scrolldown(self, e):
        self.scroll += self.scroll_step
        self.render()
    
    def windowresize(self, e):
        self.width = e.width
        self.height = e.height
        self.layout(self.tokens)
    
    def layout(self, tokens):
        self.tokens = tokens
        self.display_list = Layout(tokens, self.width, self.height).display_list
        self.render()
    
    def render(self):
        self.canvas.delete("all")
        # self.canvas.create_text(200, 100, text="Hi!", font=self.font, anchor='nw')
        for x, y, text, font in self.display_list:
            if y > self.scroll + self.height: continue
            if y + self.vstep < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=text, font=font, anchor='nw')

class Layout:
    def __init__(self, tree, width=WIDTH, height=HEIGHT):
        self.display_list = []
        self.x = HSTEP
        self.y = VSTEP
        self.line = []
        self.weight = "normal"
        self.style = "roman"
        self.size = 16
        self.width = width
        self.height = height
        self.recurse(tree)
        self.flush()
    
    def recurse(self, tree):
        if isinstance(tree, TextNode):
            self.text(tree.text)
        else:
            self.open(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close(tree.tag)
    
    def open(self, tag):
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        elif tag == "br":
            self.flush()
    
    def close(self, tag):
        if tag == "i":
            self.style = "roman"
        elif tag == "b":
            self.weight = "normal"
        elif tag == "small":
            self.size += 2
        elif tag == "big":
            self.size -= 4
        elif tag == "p":
            self.flush()
            self.y += VSTEP

    def text(self, text):
        font = tkinter.font.Font(
            size=self.size,
            weight=self.weight,
            slant=self.style,
        )
        for word in text.split():
            w = font.measure(word)
            if self.x + w >= self.width - HSTEP:
                self.flush()
            self.line.append((self.x, word, font))
            self.x += w + font.measure(" ")
    
    # Called when a new line is needed
    def flush(self):
        # Align words along the line
        # Add all those words to the display list
        # Update the x and y fields
        if not self.line: return

        metrics = [font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.y + 1.2 * max_ascent

        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        
        self.x = HSTEP
        self.line = []
        max_descent = max([metric["descent"] for metric in metrics])
        self.y = baseline + 1.2 * max_descent

SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]

class ElementNode:
    def __init__(self, tag):
        self.tag = tag
        self.children = []
    
    def __repr__(self):
        return "<" + self.tag + ">"

class TextNode:
    def __init__(self, text):
        self.text = text
    
    def __repr__(self):
        return "text_node: " + self.text

def parse(tokens):
    currently_open = []
    for tok in tokens:
        implicit_tags(tok, currently_open)
        if isinstance(tok, Text):
            node = TextNode(tok.text)
            if not currently_open: continue
            currently_open[-1].children.append(node)
        elif tok.tag.startswith("!"):
            continue
        elif tok.tag.startswith("/"):
            node = currently_open.pop()
            if not currently_open: 
                return node
            currently_open[-1].children.append(node)
        elif tok.tag in SELF_CLOSING_TAGS:
            node = ElementNode(tok.tag)
            currently_open[-1].children.append(node)
        else:
            node = ElementNode(tok.tag)
            currently_open.append(node)
    while currently_open:
        node = currently_open.pop()
        if not currently_open: return node
        currently_open[-1].children.append(node)

    [print(t) for t in currently_open]
    raise Exception("Reached last token before the end of the document")

HEAD_TAGS = [
    "base", "basefont", "bgsound", "noscript",
    "link", "meta", "title", "style", "script",
]

def implicit_tags(tok, currently_open):
    tag = tok.tag if isinstance(tok, Tag) else None
    while True:
        open_tags = [node.tag for node in currently_open]
        if open_tags == [] and tag != "html":
            currently_open.append(ElementNode("html"))
        elif open_tags == ["html"] and tag not in ["head", "body", "/html"]:
            if tag in HEAD_TAGS:
                implicit = "head"
            else:
                implicit = "body"
            currently_open.append(ElementNode(implicit))
        else:
            break
        


if __name__ == "__main__":
    import sys
    headers, html = request(sys.argv[1])
    tokens = lex(html)
    tree = parse(tokens)

    browser = Browser()
    browser.layout(tree)
    tkinter.mainloop()

# List function calls and the time it takes
# import cProfile
# from pstats import SortKey
# cProfile.run('main()', sort=SortKey.CUMULATIVE)
