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
        self.children = []

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
        self.display_list = []

        self.cx = self.x
        self.cy = self.y
        self.weight = "normal"
        self.style = "roman"
        self.size = 16

        self.line = []
        self.recurse(self.node)
        self.flush()
        self.h = self.cy - self.y
    
    def draw(self, to):
        for x, y, word, font, color in self.display_list:
            to.append(DrawText(x, y, word, font, color))
    
    def recurse(self, node):
        if isinstance(node, TextNode):
            self.text(node)
        else:
            for child in node.children:
                self.recurse(child)
    
    def font(self, node):
        bold = node.style["font-weight"]
        italic = node.style["font-style"]
        if italic == "normal": italic = "roman"
        size = int(px(node.style.get("font-size")) * .75)
        return tkinter.font.Font(size=size, weight=bold, slant=italic)
    
    def text(self, node):
        font = self.font(node)
        color = node.style["color"]
        for word in node.text.split():
            w = font.measure(word)
            if self.cx + w >= self.w - HSTEP:
                self.flush()
            self.line.append((self.cx, word, font, color))
            self.cx += w + font.measure(" ")
    
    # Called when a new line is needed
    def flush(self):
        # Align words along the line
        # Add all those words to the display list
        # Update the x and y fields
        if not self.line: return

        metrics = [font.metrics() for x, word, font, color in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cy + 1.2 * max_ascent

        for x, word, font, color in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font, color))
        
        self.cx = HSTEP
        self.line = []
        max_descent = max([metric["descent"] for metric in metrics])
        self.cy = baseline + 1.2 * max_descent


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
