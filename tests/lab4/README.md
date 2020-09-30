# Functional Tests
run `python3 browser/src/browser.py https://browser.engineering/draft/html.html`
- The parser should be able to parse this page despite the self-closing tags
- The parser should still display newlines between paragraphs (added this time, but layout function has changed)

# Unit tests

def test_parser_simpleH1():
    """Parser should be able to parse a simple html structure"""
    root_node = parse(lex("<html><body><h1>Hi!</h1></body></html>"))
    assert len(root_node.children) == 1
    assert len(root_node.children[0].children) == 1
    assert len(root_node.children[0].children[0].children) == 1
    assert root_node.children[0].children[0].children[0].text == "Hi!"

def test_parser_self_closing():
    """Parser should be able to handle self-closing tags like link or meta"""
    root_node = parse(lex("<html><link /><meta /></html>"))
    assert len(root_node.children) == 2
    assert len(root_node.children[0].children) == 0
    assert len(root_node.children[1].children) == 0