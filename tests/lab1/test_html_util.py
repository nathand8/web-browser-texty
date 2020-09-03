from src.util.html_util import *

def test_stripTags_example():
    assert stripTags("<html><body>Hello</body></html>") == "Hello"
    assert stripTags("<!doctype html><script> something </script>") == " something "