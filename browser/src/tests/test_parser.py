import io
import pytest
import mock

from src.browser import *

# ========== Test parser ==========
def test_parser_simpleH1():
    """Parser should be able to parse a simple html structure"""
    root_node = parse(lex("<html><body><h1>Hi!</h1></body></html>"))
    assert len(root_node.children) == 1
    assert len(root_node.children[0].children) == 1
    assert len(root_node.children[0].children[0].children) == 1
    assert root_node.children[0].children[0].children[0].text == "Hi!"

def test_parser_self_closing():
    """Parser should be able to handle self-closing tags like link or meta"""
    root_node = parse(lex("<html><link><meta></html>"))
    assert len(root_node.children) == 2
    assert len(root_node.children[0].children) == 0
    assert len(root_node.children[1].children) == 0

def test_parser_self_closing_with_attributes():
    """Parser should be able to handle self-closing tags like link or meta with attributes"""
    root_node = parse(lex('<html><link /><meta charset="utf-8" /></html>'))
    assert len(root_node.children) == 2
    assert len(root_node.children[0].children) == 0
    assert len(root_node.children[1].children) == 0

def test_parser_doctype():
    """Parser should safely ignore the !DOCTYPE tag"""
    root_node = parse(lex('<!DOCTYPE><html>Hi</html>'))
    assert len(root_node.children) == 1