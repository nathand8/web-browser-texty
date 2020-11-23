from src.util.helpers import relative_url

def test_complete_urls():
    url1 = "http://something.com/another/layer.html"
    assert(relative_url(url1, "") == url1)
    url2 = "https://secure.com/url/layered.html"
    assert(relative_url(url2, "") == url2)

def test_absolute_urls():
    current = "http://domain.com/something/another.html"
    url1 = "/garbage/script.js"
    expected = "http://domain.com" + url1
    assert(relative_url(url1, current) == expected)

def test_relative_urls():
    current = "http://domain.com/something/another.html"
    url1 = "script.js"
    expected = "http://domain.com/something/script.js"
    assert(relative_url(url1, current) == expected)

def test_backpath_urls():
    current = "http://domain.com/something/another.html"
    url1 = "../script.js"
    expected = "http://domain.com/script.js"
    assert(relative_url(url1, current) == expected)

    current = "http://domain.com/base/deep/nested/something/another.html"
    url1 = "../../../script.js"
    expected = "http://domain.com/base/script.js"
    assert(relative_url(url1, current) == expected)