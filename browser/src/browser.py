import tkinter
from src.connection import request
from src.lexer import lex
from src.layout import DocumentLayout, VSTEP, HSTEP, WIDTH, HEIGHT
from src.parser import parse, tree_to_string, ElementNode, TextNode
from src.css_parser import CSSParser
from src.util.helpers import find_links, relative_url

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
    
    def layout(self, tree=None):
        if not tree:
            tree = self.cached_tree
        else:
            self.cached_tree = tree
        document = DocumentLayout(tree)
        document.layout(width=self.width)
        self.max_y = document.h

        self.display_list = []
        document.draw(self.display_list)
        self.render()
    
    def render(self):
        self.canvas.delete("all")
        # self.canvas.create_text(200, 100, text="Hi!", font=self.font, anchor='nw')
        for cmd in self.display_list:
            if cmd.y1 > self.scroll + self.height: continue
            if cmd.y2 < self.scroll: continue
            cmd.draw(self.scroll, self.canvas)

    def load(self, url):
        header, body = request(url)
        nodes = parse(lex(body))

        with open("browser/src/browser.css") as f:
            browser_style = f.read()
            rules = CSSParser(browser_style).parse()
        for link in find_links(nodes, []):
            header, body = request(relative_url(link, url))
            rules.extend(CSSParser(body).parse())
        
        # tree_to_string(nodes)
        self.rules = rules
        rules.sort(key=lambda selector_body: selector_body[0].priority(), reverse=True)
        style(nodes, None, rules)
        self.layout(nodes)

        
INHERITED_PROPERTIES = {
    "font-style": "normal",
    "font-weight": "normal",
    "font-size": "16px",
}

def style(node, parent, rules):
    if isinstance(node, TextNode):
        node.style = parent.style
    else:
        for selector, pairs in rules:
            if selector.matches(node):
                for property in pairs:
                    if property not in node.style:
                        node.style[property] = pairs[property]
        for property, default in INHERITED_PROPERTIES.items():
            if property not in node.style:
                if parent:
                    node.style[property] = parent.style[property]
                else:
                    node.style[property] = default
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
