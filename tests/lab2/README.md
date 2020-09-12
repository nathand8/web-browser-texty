Unit tests:
- I've only added the new unit tests for lab 2 to this folder
- Run "pytest -v browser/"

Functional tests:
- Run "python3 browser/src/browser.py http://www.zggdwx.com/xiyou/1.html"
    - Look at the output in the window
    - Make sure chinese characters are displayed
    - Press down to scroll down the page
    - Resize the window

- Run "python3 browser/src/browser.py http://example.org/"
    - Make sure that the body shows up in the tkinter window and not the html head
    - Press down and make sure it scrolls
    - Make sure there's no duplicate text or overlapping text

- Run "python3 browser/src/browser.py https://docs.python.org/3/library/unittest.mock.html"
    - Scroll through quite a bit, hold down the down arrow. Make sure the "scroll down" logging continues to increment.