import tkinter
from src.connection import request
from src.lexer import lex
from src.layout import DocumentLayout, VSTEP, HSTEP, WIDTH, HEIGHT, find_layout, InputLayout
from src.parser import parse, tree_to_string, ElementNode, TextNode
from src.css_parser import CSSParser
from src.util.helpers import find_links, relative_url, is_link, find_inputs

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
        self.window.bind("<Button-1>", self.handle_click)
        self.window.bind("<Key>", self.keypress)
        self.window.bind("<Return>", self.pressenter)
        self.width = WIDTH
        self.height = HEIGHT
        self.hstep = HSTEP
        self.vstep = VSTEP
        self.scroll_step = SCROLL_STEP
        self.history = []
        self.focus = None
        self.address_bar = ""

        # http://www.zggdwx.com/
    
    def scrollup(self, e):
        self.scroll -= self.scroll_step
        self.scroll = min(self.scroll, self.max_y)
        self.scroll = max(0, self.scroll)
        self.render()

    def scrolldown(self, e):
        self.scroll += self.scroll_step
        self.scroll = min(self.scroll, self.max_y)
        self.scroll = max(0, self.scroll)
        self.render()
    
    def windowresize(self, e):
        self.width = e.width
        self.height = e.height
        self.layout()
    
    def keypress(self, e):
        if not (len(e.char) == 1 and 0x20 <= ord(e.char) < 0x7f):
            return
        if not self.focus:
            return
        elif self.focus == "address bar":
            self.address_bar += e.char
            self.render()
        else:
            self.focus.node.attributes["value"] += e.char
            self.layout(self.document.node)
    
    def pressenter(self, e):
        if self.focus == "address bar":
            self.focus = None
            self.load(self.address_bar)
        elif isinstance(self.focus, InputLayout):
            self.submit_form(self.focus.node)
    
    def handle_click(self, e):
        self.focus = None
        if e.y < 60: # Browser chrome
            if 10 <= e.x < 35 and 10 <= e.y < 50:
                self.go_back()
            elif 50 <= e.x < 790 and 10 <= e.y < 50:
                self.focus = "address bar"
                self.address_bar = ""
                self.render()
        else:
            x, y = e.x, e.y + self.scroll - 60
            obj = find_layout(x, y, self.document)
            if not obj: return
            elt = obj.node
            while elt:
                if isinstance(elt, TextNode):
                    pass
                elif is_link(elt):
                    url = relative_url(elt.attributes["href"], self.url)
                    self.load(url)
                elif elt.tag == "input":
                    elt.attributes["value"] = ""
                    self.focus = obj
                    self.layout(self.document.node)
                elif elt.tag == "button":
                    self.submit_form(elt)
                elt = elt.parent

    def submit_form(self, elt):
        while elt and elt.tag != "form":
            elt = elt.parent
        if not elt: return
        inputs = find_inputs(elt, [])
        body = ""
        for input in inputs:
            name = input.attributes["name"]
            value = input.attributes.get("value", "")
            body += "&" + name + "=" + value.replace(" ", "%20")
        body = body[1:]
    
        url = relative_url(elt.attributes["action"], self.url)
        self.load(url, body=body)

    
    def layout(self, tree=None):
        if not tree:
            tree = self.cached_tree
        else:
            self.cached_tree = tree
        self.document = DocumentLayout(tree)
        self.document.layout(width=self.width)
        self.max_y = self.document.h

        self.display_list = []
        self.document.draw(self.display_list)
        self.render()
    
    def render(self):
        self.canvas.delete("all")
        for cmd in self.display_list:
            if cmd.y1 > self.scroll + self.height - 60: continue
            if cmd.y2 < self.scroll: continue
            cmd.draw(self.scroll - 60, self.canvas)

        self.canvas.create_rectangle(0, 0, 800, 60, width=0, fill='light gray')
    
        self.canvas.create_rectangle(50, 10, 790, 50)
        font = tkinter.font.Font(family="Courier", size=30)
        self.canvas.create_text(55, 15, anchor='nw', text=self.address_bar, font=font)

        self.canvas.create_rectangle(10, 10, 35, 50)
        self.canvas.create_polygon(15, 30, 30, 15, 30, 45, fill='black')

        if self.focus == "address bar":
            w = font.measure(self.address_bar)
            self.canvas.create_line(55 + w, 15, 55 + w, 45)
        elif isinstance(self.focus, InputLayout):
            text = self.focus.node.attributes.get("value", "")
            x = self.focus.x + self.focus.font.measure(text)
            y = self.focus.y - self.scroll + 60
            self.canvas.create_line(x, y, x, y + self.focus.h)

    def load(self, url, body=None):
        self.address_bar = url
        self.url = url
        self.history.append(url)
        header, body = request(url, body)
        nodes = parse(lex(body))

        with open("browser/src/browser.css") as f:
            browser_style = f.read()
            rules = CSSParser(browser_style).parse()
        for link in find_links(nodes, []):
            header, body = request(relative_url(link, url))
            rules.extend(CSSParser(body).parse())
        
        # tree_to_string(nodes)
        rules.sort(key=lambda selector_body: selector_body[0].priority(), reverse=True)
        style(nodes, None, rules)
        self.layout(nodes)
    
    def go_back(self):
        if len(self.history) > 2:
            self.history.pop()
            back = self.history.pop()
            self.load(back)

        
INHERITED_PROPERTIES = {
    "font-style": "normal",
    "font-weight": "normal",
    "font-size": "16px",
    "color": "black"
}

def style(node, parent, rules):
    if isinstance(node, TextNode):
        node.style = parent.style
    else:
        for selector, pairs in rules:
            if selector.matches(node):
                for prop in pairs:
                    if prop not in node.style:
                        node.style[prop] = pairs[prop]
        for prop, default in INHERITED_PROPERTIES.items():
            if prop not in node.style:
                if parent:
                    node.style[prop] = parent.style[prop]
                else:
                    node.style[prop] = default
        for child in node.children:
            style(child, node, rules)

if __name__ == "__main__":
    import sys
    browser = Browser()
    browser.load(sys.argv[1])
    tkinter.mainloop()




# List function calls and the time it takes
# import cProfile
# from pstats import SortKey
# cProfile.run('main()', sort=SortKey.CUMULATIVE)
