import tkinter
import dukpy
from src.connection import request
from src.lexer import lex
from src.layout import DocumentLayout, VSTEP, HSTEP, WIDTH, HEIGHT, find_layout, InputLayout
from src.parser import parse, tree_to_string, ElementNode, TextNode
from src.css_parser import CSSParser
from src.util.helpers import find_links, find_scripts, relative_url, is_link, find_inputs
from src.timer import Timer

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
        self.timer = Timer()
        self.cookies = {}

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
        if e.width < 10: return
        if e.width == self.width and e.height == self.height: return
        self.width = e.width
        self.height = e.height
        print("Layout called from windowresize")
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
            self.dispatch_event("change", self.focus.node)
            print("Layout called from keypress")
            self.reflow(self.focus)
    
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
            if elt and self.dispatch_event("click", elt): return
            while elt:
                if isinstance(elt, TextNode):
                    pass
                elif is_link(elt):
                    url = relative_url(elt.attributes["href"], self.url)
                    self.load(url)
                elif elt.tag == "input":
                    elt.attributes["value"] = ""
                    self.focus = obj
                    print("Layout called from handle_click in input elt")
                    return self.reflow(self.focus)
                elif elt.tag == "button":
                    self.submit_form(elt)
                elt = elt.parent

    def submit_form(self, elt):
        while elt and elt.tag != "form":
            elt = elt.parent
        if not elt: return
        if self.dispatch_event("submit", elt): return
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
        self.timer.start("Layout Initialization")
        if not tree:
            tree = self.cached_tree
        else:
            self.cached_tree = tree
        self.document = DocumentLayout(tree)
        self.reflow(self.document)
    
    def reflow(self, obj):
        self.timer.start("Style")
        style(obj.node, obj.parent, self.rules)
        self.timer.start("Layout (phase 1A)")
        obj.size()
        self.timer.start("Layout (phase 1B)")
        while obj.parent:
            obj.parent.compute_height()
            obj = obj.parent
        self.timer.start("Layout (phase 2)")
        self.document.position()
        self.timer.start("Display List")
        self.display_list = []
        self.document.draw(self.display_list)
        self.max_y = self.document.h
        self.render()
    
    def render(self):
        self.canvas.delete("all")
        self.timer.start("Rendering")
        for cmd in self.display_list:
            if cmd.y1 > self.scroll + self.height - 60:
                continue
            if cmd.y2 < self.scroll:
                continue
            cmd.draw(self.scroll - 60, self.canvas)

        self.timer.start("Chrome")
        self.canvas.create_rectangle(0, 0, 800, 60, width=0, fill='light gray')
    
        self.canvas.create_rectangle(50, 10, 790, 50)
        font = tkinter.font.Font(family="Courier", size=30)
        self.canvas.create_text(55, 15, anchor='nw', text=self.address_bar, font=font)

        self.canvas.create_rectangle(10, 10, 35, 50)
        self.canvas.create_polygon(15, 30, 30, 15, 30, 45, fill='black')
        self.timer.stop()

        if self.focus == "address bar":
            w = font.measure(self.address_bar)
            self.canvas.create_line(55 + w, 15, 55 + w, 45)
        elif isinstance(self.focus, InputLayout):
            text = self.focus.node.attributes.get("value", "")
            x = self.focus.x + self.focus.font.measure(text)
            y = self.focus.y - self.scroll + 60
            self.canvas.create_line(x, y, x, y + self.focus.h)
    
    def cookie_string(self):
        cookie_string = ""
        for key, value in self.cookies.items():
            cookie_string += "&" + key + "=" + value
        return cookie_string[1:]

    def load(self, url, body=None):
        self.address_bar = url
        self.url = url
        self.history.append(url)
        self.timer.start("Downloading")
        req_headers = {}
        if self.cookie_string():
            req_headers["Cookie"] = self.cookie_string()
        headers, body = request(url, headers=req_headers, payload=body)
        if "set-cookie" in headers:
            kv, *params = headers["set-cookie"].split(";")
            key, value = kv.split("=", 1)
            self.cookies[key] = value
        self.timer.start("Parsing HTML")
        self.nodes = parse(lex(body))

        self.timer.start("Parsing CSS")
        with open("browser/src/browser.css") as f:
            browser_style = f.read()
            rules = CSSParser(browser_style).parse()
        for link in find_links(self.nodes, []):
            headers, body = request(relative_url(link, url), headers=req_headers)
            rules.extend(CSSParser(body).parse())

        # tree_to_string(self.nodes)
        rules.sort(key=lambda selector_body: selector_body[0].priority(), reverse=True)
        self.rules = rules

        self.timer.start("Running JS")
        self.setup_js()
        for script in find_scripts(self.nodes, []):
            header, body = request(relative_url(script, self.history[-1]), headers=req_headers)
            try:
                # print("Script returned: ", self.js_environment.evaljs(body))
                self.js_environment.evaljs(body)
            except dukpy.JSRuntimeError as e:
                print("Script", script, "crashed", e)

        print("Layout called from load")
        self.layout(self.nodes)
    
    def go_back(self):
        if len(self.history) > 2:
            self.history.pop()
            back = self.history.pop()
            self.load(back)
        
    def setup_js(self):
        self.node_to_handle = {}
        self.handle_to_node = {}
        self.js_environment = dukpy.JSInterpreter()
        self.js_environment.export_function("log", print)
        self.js_environment.export_function("querySelectorAll", self.js_querySelectorAll)
        self.js_environment.export_function("getAttribute", self.js_getAttribute)
        self.js_environment.export_function("innerHTML", self.js_innerHTML)
        with open("browser/src/runtime.js") as f:
            self.js_environment.evaljs(f.read())

    def js_querySelectorAll(self, sel):
        selector, _ = CSSParser(sel + "{").selector(0)
        elts = find_selected(self.nodes, selector, [])
        return [self.make_handle(elt) for elt in elts]
    
    def make_handle(self, elt):
        if id(elt) not in self.node_to_handle:
            handle = len(self.node_to_handle)
            self.node_to_handle[id(elt)] = handle
            self.handle_to_node[handle] = elt
        else:
            handle = self.node_to_handle[id(elt)]
        return handle
    
    def js_getAttribute(self, handle, attr):
        elt = self.handle_to_node[handle]
        return elt.attributes.get(attr, None)
    
    def js_innerHTML(self, handle, s):
        doc = parse(lex("<html><body>" + s + "</body></html>"))
        new_nodes = doc.children[0].children
        elt = self.handle_to_node[handle]
        elt.children = new_nodes
        for child in elt.children:
            child.parent = elt
        print("Layout called from js_innerHTML")
        self.reflow(layout_for_node(self.document, elt))

    def dispatch_event(self, type, elt):
        handle = self.make_handle(elt)
        code = "__runHandlers({}, \"{}\")".format(handle, type)
        do_default = self.js_environment.evaljs(code)
        return not do_default


def find_selected(node, sel, out):
    if not isinstance(node, ElementNode): return
    if sel.matches(node):
        out.append(node)
    for child in node.children:
        find_selected(child, sel, out)
    return out

def layout_for_node(tree, node):
    if tree.node == node:
        return tree
    for child in tree.children:
        out = layout_for_node(child, node)
        if out: return out

        
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
