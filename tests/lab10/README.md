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