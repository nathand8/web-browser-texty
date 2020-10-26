from src.parser import TextNode, ElementNode
import tkinter
import tkinter.font


# Constants for the layout
WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18

def px(s):
    if s.endswith("px"):
        return int(s[:-2])
    else:
        return 0

class DocumentLayout:
    def __init__(self, node):
        self.node = node
        self.parent = None
        self.children = []

        self.mt = self.mr = self.mb = self.ml = 0
        self.bt = self.br = self.bb = self.bl = 0
        self.pt = self.pr = self.pb = self.pl = 0

    def layout(self, width=WIDTH):
        self.w = width
        child = BlockLayout(self.node, self)
        self.children.append(child)
        child.x = self.x = 3 # For some reason the letters are getting cut off on the far left when we start at 0
        child.y = self.y = 0
        child.layout()
        self.h = child.h
    
    def draw(self, to):
        self.children[0].draw(to)
        

class BlockLayout:
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent
        self.children = []

        self.x = -1
        self.y = -1
        self.w = -1
        self.h = -1

        self.mt = self.mr = self.mb = self.ml = -1
        self.bt = self.br = self.bb = self.bl = -1
        self.pt = self.pr = self.pb = self.pl = -1
    
    def layout(self):
        self.mt = px(self.node.style.get("margin-top", "0px"))
        self.bt = px(self.node.style.get("border-top-width", "0px"))
        self.pt = px(self.node.style.get("padding-top", "0px"))
        self.mr = px(self.node.style.get("margin-right", "0px"))
        self.br = px(self.node.style.get("border-right-width", "0px"))
        self.pr = px(self.node.style.get("padding-right", "0px"))
        self.mb = px(self.node.style.get("margin-bottom", "0px"))
        self.bb = px(self.node.style.get("border-bottom-width", "0px"))
        self.pb = px(self.node.style.get("padding-bottom", "0px"))
        self.ml = px(self.node.style.get("margin-left", "0px"))
        self.bl = px(self.node.style.get("border-left-width", "0px"))
        self.pl = px(self.node.style.get("padding-left", "0px"))

        if self.has_block_children():
            for child in self.node.children:
                if isinstance(child, TextNode): continue
                self.children.append(BlockLayout(child, self))
        else:
            self.children.append(InlineLayout(self.node, self))
        
        # Width is set by parent
        self.w = self.parent.w - self.parent.pl - self.parent.pr \
            - self.parent.bl - self.parent.br \
            - self.ml - self.mr

        # Height is determined by children's heights
        self.y += self.mt
        self.x += self.ml
        y = self.y
        for child in self.children:
            child.x = self.x + self.pl + self.bl
            child.y = y
            child.layout()
            y += child.h + child.mt + child.mb
        self.h = y - self.y

    def has_block_children(self):
        for child in self.node.children:
            if isinstance(child, TextNode):
                if not child.text.isspace():
                    return False
            elif child.style.get("display", "block") == "inline":
                return False
        return True
    
    def draw(self, to):
        for child in self.children:
            if self.node.tag == "pre":
                x2, y2 = self.x + self.w, self.y + self.h
                to.append(DrawRect(self.x, self.y, x2, y2, "gray"))
            child.draw(to)

class InlineLayout:
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent
        self.children = [LineLayout(self.node, self)]

        self.x = -1
        self.y = -1
        self.w = -1
        self.h = -1

        self.mt = self.mr = self.mb = self.ml = 0
        self.bt = self.br = self.bb = self.bl = 0
        self.pt = self.pr = self.pb = self.pl = 0

    def layout(self):
        self.w = self.parent.w - self.parent.pl - self.parent.pr \
            - self.parent.bl - self.parent.br

        self.cy = self.y

        self.recurse(self.node)
        self.flush()
        self.h = self.cy - self.y

        # Get rid of one extra line at the end
        self.children.pop()
    
    def draw(self, to):
        for line in self.children:
            line.draw(to)
    
    def recurse(self, node):
        if isinstance(node, ElementNode):
            if node.tag == "input":
                self.input(node)
            else:
                for child in node.children:
                    self.recurse(child)
        else:
            self.text(node)
    
    def input(self, node):
        child = InputLayout(node)
        child.layout()
        if self.children[-1].cx + child.w > self.w:
            self.flush()
        self.children[-1].append(child)
    
    def text(self, node):
        for word in node.text.split():
            child = TextLayout(node, word)
            child.layout()
            if self.children[-1].cx + child.w > self.w:
                self.flush()
            self.children[-1].append(child)
    
    # Called when a new line is needed
    def flush(self):
        child = self.children[-1]
        child.x = self.x
        child.y = self.cy
        child.layout()
        self.cy += child.h
        self.children.append(LineLayout(self.node, self))

class LineLayout:
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent
        self.children = []
        self.cx = 0
    
    def append(self, child):
        self.children.append(child)
        child.parent = self
        self.cx += child.w + child.font.measure(" ")
    
    def layout(self):
        self.w = self.parent.w

        if not self.children:
            self.h = 0
            return

        for word in self.children:
            word.layout()

        metrics = [word.font.metrics() for word in self.children]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.y + 1.2 * max_ascent

        x = self.x
        for word in self.children:
            word.y = baseline - word.font.metrics("ascent")
            word.x = x
            x += word.w + word.font.measure(" ")
        
        self.h = max([word.h for word in self.children])
    
    def draw(self, to):
        for word in self.children:
            word.draw(to)


class TextLayout:
    def __init__(self, node, word):
        self.node = node
        self.children = []
        self.word = word

    def layout(self):
        weight = self.node.style["font-weight"]
        style = self.node.style["font-style"]
        if style == "normal": style = "roman"
        size = int(px(self.node.style["font-size"]) * .75)
        self.font = tkinter.font.Font(size=size, weight=weight, slant=style)

        self.w = self.font.measure(self.word)
        self.h = self.font.metrics('linespace')
    
    def draw(self, to):
        color = self.node.style["color"]
        to.append(DrawText(self.x, self.y, self.word, self.font, color))

class InputLayout: 
    def __init__(self, node):
        self.node = node
        self.children = []
    
    def layout(self):
        self.w = 200
        self.h = 20

        weight = self.node.style["font-weight"]
        style = self.node.style["font-style"]
        if style == "normal": style = "roman"
        size = int(px(self.node.style["font-size"]) * .75)
        self.font = tkinter.font.Font(size=size, weight=weight, slant=style)
    
    def draw(self, to):
        x1, x2 = self.x, self.x + self.w
        y1, y2 = self.y, self.y + self.h
        to.append(DrawRect(x1, y1, x2, y2, "light gray"))

        text = self.node.attributes.get("value", "")
        color = self.node.style["color"]
        to.append(DrawText(self.x, self.y, text, self.font, color))


class DrawText:
    def __init__(self, x1, y1, text, font, color):
        self.x1 = x1
        self.y1 = y1
        self.y2 = y1 + font.metrics("linespace")
        self.text = text
        self.font = font
        self.color = color
    
    def draw(self, scroll, canvas):
        canvas.create_text(
            self.x1, self.y1 - scroll,
            text=self.text,
            font=self.font,
            fill=self.color,
            anchor='nw'
        )
    
class DrawRect:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
    
    def draw(self, scroll, canvas):
        canvas.create_rectangle(
            self.x1, self.y1 - scroll,
            self.x2, self.y2 - scroll,
            width=0,
            fill=self.color
        )

def find_layout(x, y, tree):
    for child in reversed(tree.children):
        result = find_layout(x, y, child)
        if result: return result
    if tree.x <= x < tree.x + tree.w and \
       tree.y <= y < tree.y + tree.h:
        return tree
