import pytest
from src.util.url_util import *

def test_splitURL_example():
    scheme, host, port, path = splitURL("http://example.org/index.html")
    assert(scheme == "http")
    assert(host == "example.org")
    assert(port == 80) # Default port should be 80
    assert(path == "/index.html")

def test_splitURL_https():
    scheme, host, port, path = splitURL("https://example.org/index.html")
    assert(scheme == "https")
    assert(port == 443) # Encrypted port should be 80

def test_splitURL_custom_port():
    scheme, host, port, path = splitURL("http://example.org:8080/index.html")
    assert(scheme == "http")
    assert(host == "example.org")
    assert(port == 8080)
    assert(path == "/index.html")

def test_splitURL_custom_port_https():
    scheme, host, port, path = splitURL("https://example.org:8080/index.html")
    assert(scheme == "https")
    assert(host == "example.org")
    assert(port == 8080)
    assert(path == "/index.html")

def test_splitURL_empty_path():
    scheme, host, port, path = splitURL("http://example.org/")
    assert(path == "/")

def test_splitURL_bad_scheme():
    with pytest.raises(AssertionError) as error:
        splitURL("ftp://example.org/index.html")
    assert "Unknown scheme" in str(error.value)
