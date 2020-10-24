import tkinter
from src.connection import request
from src.lexer import lex
from src.layout import DocumentLayout, VSTEP, HSTEP, WIDTH, HEIGHT, find_layout
from src.parser import parse, tree_to_string, ElementNode, TextNode
from src.css_parser import CSSParser
from src.util.helpers import find_links, relative_url, is_link

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
        self.width = WIDTH
        self.height = HEIGHT
        self.hstep = HSTEP
        self.vstep = VSTEP
        self.scroll_step = SCROLL_STEP

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
    
    def handle_click(self, e):
        x, y = e.x, e.y + self.scroll
        obj = find_layout(x, y, self.document)
        if not obj: return
        elt = obj.node
        while elt and not is_link(elt):
            elt = elt.parent
        if elt:
            url = relative_url(elt.attributes["href"], self.url)
            self.load(url)
    
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
        # self.canvas.create_text(200, 100, text="Hi!", font=self.font, anchor='nw')
        for cmd in self.display_list:
            if cmd.y1 > self.scroll + self.height: continue
            if cmd.y2 < self.scroll: continue
            cmd.draw(self.scroll, self.canvas)

    def load(self, url):
        self.url = url
        header, body = request(url)
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
