from src.lexer import Tag, Text

SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]

class ElementNode:
    def __init__(self, tag, attributes={}):
        self.tag = tag
        self.attributes = attributes
        self.children = []
        self.style = {}
        for pair in self.attributes.get("style", "").split(";"):
            if ":" not in pair: continue
            prop, val = pair.split(":")
            self.style[prop.strip().lower()] = val.strip()
    
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
            node = ElementNode(tok.tag, tok.attributes)
            currently_open[-1].children.append(node)
        else:
            node = ElementNode(tok.tag, tok.attributes)
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
            currently_open.append(ElementNode("html", {}))
        elif open_tags == ["html"] and tag not in ["head", "body", "/html"]:
            if tag in HEAD_TAGS:
                implicit = "head"
            else:
                implicit = "body"
            currently_open.append(ElementNode(implicit, {}))
        else:
            break

def tree_to_string(tree, indent=""):
    print(indent, tree)
    if isinstance(tree, ElementNode):
        for node in tree.children:
            tree_to_string(node, indent + "  ")