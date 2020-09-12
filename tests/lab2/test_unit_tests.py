import io
import pytest
import mock

from src.browser import *

# ========== Test getBody ===========
def test_getBody_example():
    assert getBody("<html><body>Some <div>elements</div> </body></html>") == "<body>Some <div>elements</div> </body>"

# ========= Test Browser.layout =========
def test_browser_layout():
    b = Browser()
    b.width = 7
    b.height = 20
    b.hstep = 2
    b.vstep = 3
    b.layout("hello")
    assert b.display_list == [
        (2, 3, "h"), (4, 3, "e"),
        (2, 6, "l"), (4, 6, "l"),
        (2, 9, "o")
    ]

def test_browser_layout_strip_surrounding_whitespace():
    b = Browser()
    b.layout("\n\t \ra\n\t \r")
    assert len(b.display_list) == 1

def test_browser_layout_set_text():
    b = Browser()
    b.text = "unset"
    b.layout("set")
    assert b.text == "set"

def test_browser_layout_set_text():
    b = Browser()
    b.text = "unset"
    b.layout("set")
    assert b.text == "set"

def test_browser_window_resize():
    b = Browser()
    b.width = 0
    b.height = 0
    mockEvent = mock.Mock()
    mockEvent.width = 10
    mockEvent.height = 5
    b.windowresize(mockEvent)
    assert b.width == 10
    assert b.height == 5

def test_browser_scroll_down():
    b = Browser()
    b.scroll_step = 10
    b.scroll = 2
    b.scrolldown(None)
    assert b.scroll == 12