import tkinter
import tkinter.font
import re
from src.connection import request
from src.lexer import lex
from src.layout import Layout, parse

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
        self.display_list = Layout(tokens, self.width, self.height, self.hstep, self.vstep).display_list
        self.render()
    
    def render(self):
        self.canvas.delete("all")
        # self.canvas.create_text(200, 100, text="Hi!", font=self.font, anchor='nw')
        for x, y, text, font in self.display_list:
            if y > self.scroll + self.height: continue
            if y + self.vstep < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=text, font=font, anchor='nw')

        

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
