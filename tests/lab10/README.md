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
