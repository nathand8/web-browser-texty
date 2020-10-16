from src.lexer import Tag, Text
import tkinter
import tkinter.font

class Layout:
    def __init__(self, tree, width, height, HSTEP, VSTEP):
        self.display_list = []
        self.hstep = HSTEP
        self.vstep = VSTEP
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
            self.y += self.vstep

    def text(self, text):
        font = tkinter.font.Font(
            size=self.size,
            weight=self.weight,
            slant=self.style,
        )
        for word in text.split():
            w = font.measure(word)
            if self.x + w >= self.width - self.hstep:
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
        
        self.x = self.hstep
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