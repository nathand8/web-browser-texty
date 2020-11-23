from src.parser import TextNode, ElementNode
import tkinter
import tkinter.font


# Constants for the layout
WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
INDENT = "  "

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

    def size(self, width=WIDTH):
        self.w = width
        child = BlockLayout(self.node, self)
        self.children.append(child)
        child.size()
        self.h = child.h
        # print(INDENT * get_depth(self) + "DocumentLayout size: w", self.w, ", h", self.h)
    
    def position(self):
        child = self.children[0]
        child.x = self.x = 3 # For some reason the letters are getting cut off on the far left when we start at 0
        child.y = self.y = 0
        child.position()
    
    def draw(self, to):
        self.children[0].draw(to)
        

class BlockLayout:
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent
    
    def size(self):
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

        self.children = []
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

        self.h = 0
        for child in self.children:
            child.size()
            self.h += child.mt + child.h + child.mb

        # print(INDENT * get_depth(self) + "BlockLayout size: w", self.w, ", h", self.h)
    
    def position(self):
        self.y += self.mt
        self.x += self.ml

        y = self.y
        for child in self.children:
            child.x = self.x + self.pl + self.bl
            child.y = y
            child.position()
            y += child.mt + child.h + child.mb


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

        self.x = 0
        self.y = 0

        self.mt = self.mr = self.mb = self.ml = 0
        self.bt = self.br = self.bb = self.bl = 0
        self.pt = self.pr = self.pb = self.pl = 0

    def size(self):
        self.w = self.parent.w - self.parent.pl - self.parent.pr \
            - self.parent.bl - self.parent.br

        self.h = 0
        self.recurse(self.node)
        self.flush()
        # Get rid of one extra line at the end
        self.children.pop()
        # print(INDENT * get_depth(self) + "InlineLayout size: w", self.w, ", h", self.h)
    
    def draw(self, to):
        for line in self.children:
            line.draw(to)
    
    def recurse(self, node):
        if isinstance(node, ElementNode):
            if node.tag == "input":
                self.input(node)
            elif node.tag == "button":
                self.input(node)
            else:
                for child in node.children:
                    self.recurse(child)
        else:
            self.text(node)
    
    def input(self, node):
        child = InputLayout(node)
        child.size()
        if self.children[-1].cx + child.w > self.w:
            self.flush()
        self.children[-1].append(child)
    
    def text(self, node):
        for word in node.text.split():
            child = TextLayout(node, word)
            child.size()
            if self.children[-1].cx + child.w > self.w:
                self.flush()
            self.children[-1].append(child)
    
    def flush(self):
        child = self.children[-1]
        child.size()
        self.h += child.h
        self.children.append(LineLayout(self.node, self))
    
    def position(self):
        cy = self.y
        for child in self.children:
            child.x = self.x
            child.y = cy
            child.position()
            cy += child.h

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

    def size(self):
        self.w = self.parent.w
        if not self.children:
            self.h = 0
            return
        self.metrics = [child.font.metrics() for child in self.children]
        self.max_ascent = max([metric["ascent"] for metric in self.metrics])
        self.max_descent = max([metric["descent"] for metric in self.metrics])
        self.h = 1.2 * (self.max_descent + self.max_ascent)
        # print(INDENT * get_depth(self) + "LineLayout size: w", self.w, ", h", self.h)
    
    def position(self):
        baseline = self.y + 1.2 * self.max_ascent
        cx = 0
        for child, metrics in zip(self.children, self.metrics):
            child.x = self.x + cx
            child.y = baseline - metrics["ascent"]
            cx += child.w + child.font.measure(" ")
    
    def draw(self, to):
        for word in self.children:
            word.draw(to)


class TextLayout:
    def __init__(self, node, word):
        self.node = node
        self.children = []
        self.word = word

    def size(self):
        weight = self.node.style["font-weight"]
        style = self.node.style["font-style"]
        if style == "normal": style = "roman"
        size = int(px(self.node.style["font-size"]) * .75)
        self.font = tkinter.font.Font(size=size, weight=weight, slant=style)

        self.w = self.font.measure(self.word)
        self.h = self.font.metrics('linespace')

    def position(self):
        return
    
    def draw(self, to):
        color = self.node.style["color"]
        to.append(DrawText(self.x, self.y, self.word, self.font, color))

class InputLayout: 
    def __init__(self, node):
        self.node = node
        self.children = []
    
    def size(self):
        self.w = 200
        self.h = 20

        weight = self.node.style["font-weight"]
        style = self.node.style["font-style"]
        if style == "normal": style = "roman"
        size = int(px(self.node.style["font-size"]) * .75)
        self.font = tkinter.font.Font(size=size, weight=weight, slant=style)

    def position(self):
        return
    
    def draw(self, to):
        x1, x2 = self.x, self.x + self.w
        y1, y2 = self.y, self.y + self.h
        bgcolor = "light gray" if self.node.tag == "input" else "yellow"
        to.append(DrawRect(x1, y1, x2, y2, bgcolor))

        if self.node.tag == "input":
            text = self.node.attributes.get("value", "")
        else:
            text = self.node.children[0].text

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

def get_depth(node):
    depth = 0
    while node.parent:
        depth += 1
        node = node.parent
    return depth
