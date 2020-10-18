from src.css_parser import *
from src.parser import *

def test_parser_tag_selector():
    """Parse a single rule for a tag selector"""
    css = """
    p {
        margin-top: 10px;

    }
    """
    parser = CSSParser(css)
    rules = parser.parse()
    assert len(rules) == 1
    selector = rules[0][0]
    rule = rules[0][1]
    assert isinstance(selector, TagSelector)
    assert rule['margin-top'] == "10px"

def test_parser_class_selector():
    """Parse a single rule for a class selector"""
    css = """
    .classname {
        margin-top: 10px;
    }
    """
    parser = CSSParser(css)
    rules = parser.parse()
    assert len(rules) == 1
    selector = rules[0][0]
    rule = rules[0][1]
    assert isinstance(selector, ClassSelector)
    assert rule['margin-top'] == "10px"

def test_parser_id_selector():
    """Parse a single rule for a id selector"""
    css = """
    #idname {
        margin-top: 10px;
    }
    """
    parser = CSSParser(css)
    rules = parser.parse()
    assert len(rules) == 1
    selector = rules[0][0]
    rule = rules[0][1]
    assert isinstance(selector, IdSelector)
    assert rule['margin-top'] == "10px"

def test_parser_multiple_rules():
    """Parse a single rule for a tag selector"""
    css = """
    p {
        margin-top: 10px;
        margin-bottom: 20px;
    }
    """
    parser = CSSParser(css)
    rules = parser.parse()
    assert len(rules) == 1
    rule = rules[0][1]
    assert rule['margin-top'] == "10px"
    assert rule['margin-bottom'] == "20px"

def test_parser_multiple_rules_multiple_selectors():
    """Parse a single rule for a tag selector"""
    css = """
    p {
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .classname {
        margin-left: 5px;
        margin-right: 15px;
    }
    """
    parser = CSSParser(css)
    rules = parser.parse()
    assert len(rules) == 2

def test_class_selector_matches():
    s = ClassSelector("centered")
    node1 = ElementNode("div", {"class": "centered bold"})
    node2 = ElementNode("div", {"class": "only bold"})
    assert s.matches(node1)
    assert not s.matches(node2)

def test_id_selector_matches():
    s = IdSelector("idname")
    node1 = ElementNode("div", {"id": "idname"})
    node2 = ElementNode("div", {"id": "different"})
    assert s.matches(node1)
    assert not s.matches(node2)

def test_tag_selector_matches():
    s = TagSelector("div")
    node1 = ElementNode("div")
    node2 = ElementNode("p")
    assert s.matches(node1)
    assert not s.matches(node2)