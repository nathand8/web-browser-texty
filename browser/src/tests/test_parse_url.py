from src.browser import *

def test_url_parse():
    """Should be able to parse url into 3 parts"""
    host, port, path = parse_url("http://localhost:8000/form.html")
    assert host == "localhost"
    assert port == "8000"
    assert path == "/form.html"