# Functional Tests
run `python3 browser/src/browser.py https://browser.engineering/draft/html.html`
- The parser should be able to parse this page despite the self-closing tags
- The parser should still display newlines between paragraphs (added this time, but layout function has changed)

run simple web server in the root of the directory
run `python3 browser/src/browser.py http://localhost:8000/tests/lab4/SimpleH1Parse.html`
- Hi should appear in the middle of the screen


# Unit tests

```python
def test_parser_simpleH1():
    """Parser should be able to parse a simple html structure"""
    root_node = parse(lex("<html><body><h1>Hi!</h1></body></html>"))
    assert len(root_node.children) == 1
    assert len(root_node.children[0].children) == 1
    assert len(root_node.children[0].children[0].children) == 1
    assert root_node.children[0].children[0].children[0].text == "Hi!"

def test_parser_self_closing():
    """Parser should be able to handle self-closing tags like link or meta"""
    root_node = parse(lex("<html><head><link><meta></head></html>"))
    head = root_node.children[0]
    assert len(head.children) == 2
    assert len(head.children[0].children) == 0
    assert len(head.children[1].children) == 0

def test_parser_self_closing_with_attributes():
    """Parser should be able to handle self-closing tags like link or meta with attributes"""
    root_node = parse(lex('<html><head><link /><meta charset="utf-8" /></head></html>'))
    head = root_node.children[0]
    assert len(head.children) == 2
    assert len(head.children[0].children) == 0
    assert len(head.children[1].children) == 0

def test_parser_doctype():
    """Parser should safely ignore the !DOCTYPE tag"""
    root_node = parse(lex('<!DOCTYPE><html>Hi</html>'))
    assert len(root_node.children) == 1

def test_parser_no_html():
    """Parser should add the implicit html tag"""
    root_node = parse(lex('<body>Hi</body>'))
    assert root_node.tag == "html"

def test_parser_html_only():
    """Parser should not add implicit head or body tags for an empty html element"""
    root_node = parse(lex('<html></html>'))
    assert root_node.tag == "html"
    assert len(root_node.children) == 0

def test_parser_implicit_head():
    """Parser should add implicit head tag link element"""
    root_node = parse(lex('<html><link /></html>'))
    head = root_node.children[0]
    assert head.tag == "head"
    assert head.children[0].tag == "link"

def test_parser_implicit_body():
    """Parser should add implicit body tag link element"""
    root_node = parse(lex('<html><div>Hi</div></html>'))
    body = root_node.children[0]
    assert body.tag == "body"
    assert body.children[0].tag == "div"

def test_parser_implicit_all():
    """Parser should be able to add implicit html, head, and body"""
    root_node = parse(lex('<link /></head><div>Hi</div>'))
    # Expected Tree: <html><head><link /></head><body><div>Hi</div></body></html>
    assert root_node.tag == "html"
    assert len(root_node.children) == 2
    head = root_node.children[0]
    assert head.tag == "head"
    assert head.children[0].tag == "link"
    body = root_node.children[1]
    assert body.tag == "body"
    assert body.children[0].tag == "div"
```