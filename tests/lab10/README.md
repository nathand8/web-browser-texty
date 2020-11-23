# Unit tests

```
def test_backpath_urls():
    current = "http://domain.com/something/another.html"
    url1 = "../script.js"
    expected = "http://domain.com/script.js"
    assert(relative_url(url1, current) == expected)

    current = "http://domain.com/base/deep/nested/something/another.html"
    url1 = "../../../script.js"
    expected = "http://domain.com/base/script.js"
    assert(relative_url(url1, current) == expected
```
- This ensures that link href like "../book.css" are handled correctly

# Functional Tests
Run `python -m http.server 8000`
Run `python3 browser/src/browser.py http://localhost:8000/tests/lab10/example.html`
- Click the "Click me" button multiple times. The last paragraph should move down as the first paragraph gets bigger
- Scrolling up and down should still work
- The timing on the 2nd Layout phase should remain minimal

Run `python3 browser/src/browser.py https://browser.engineering/index.html`
- Click on the url and type in letters, there shouldn't be much of a lag
- Only "Rendering" and "Chrome" timers should repeat on keypress
- Click on the name input and type letters, there shouldn't be much lag
- The Style, Layout phase 1A, Layout phase 1B and layout phase 2 should all take less than 0.01 combined
- Scroll down and up, only the "Chrome" and "Rendering" timers should fire
- Scrolling should be pretty smooth

Run `python3 server.py`
Run `python3 browser/src/browser.py http://localhost:8000/`
- The guestbook should still work, submit a few inputs to be sure
- A keypress in the name field should trigger layout phases that are very quick (< 0.001 s)