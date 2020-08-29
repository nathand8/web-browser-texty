import pytest
from src.util.url_util import *

def test_splitURL_example():
    protocol, host, port, path = splitURL("http://example.org/index.html")
    assert(protocol == "http")
    assert(host == "example.org")
    assert(port == 80) # Default port should be 80
    assert(path == "/index.html")

def test_splitURL_custom_port():
    protocol, host, port, path = splitURL("http://example.org:8080/index.html")
    assert(protocol == "http")
    assert(host == "example.org")
    assert(port == 8080)
    assert(path == "/index.html")

def test_splitURL_empty_path():
    protocol, host, port, path = splitURL("http://example.org/")
    assert(path == "/")

def test_splitURL_bad_protocol():
    with pytest.raises(AssertionError) as error:
        splitURL("https://example.org/index.html")
    assert "Unknown protocol" in str(error.value)
