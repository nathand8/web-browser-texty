import tkinter
from src.connection import request
from src.lexer import lex
from src.layout import DocumentLayout, parse, VSTEP, HSTEP, WIDTH, HEIGHT, tree_to_string

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
        self.tree = []

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
        self.layout(self.tree)
    
    def layout(self, tree):
        self.tree = tree
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

        

if __name__ == "__main__":
    import sys
    headers, html = request(sys.argv[1])
    tokens = lex(html)
    tree = parse(tokens)
    # tree_to_string(tree)

    browser = Browser()
    browser.layout(tree)
    tkinter.mainloop()




# List function calls and the time it takes
# import cProfile
# from pstats import SortKey
# cProfile.run('main()', sort=SortKey.CUMULATIVE)
