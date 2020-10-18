def debugCssParser(*args):
    pass
    # print(*args)

class TagSelector:
    def __init__(self, tag):
        self.tag = tag

    def matches(self, node):
        return self.tag == node.tag
    
    def priority(self):
        return 1

class ClassSelector:
    def __init__(self, cls):
        self.cls = cls
    
    def matches(self, node):
        return self.cls in node.attributes.get("class", "").split()

    def priority(self):
        return 16

class IdSelector:
    def __init__(self, id):
        self.id = id

    def matches(self, node):
        return self.id == node.attributes.get("id", "")

    def priority(self):
        return 256

class CSSParser:

    def __init__(self, s):
        self.s = s
    
    def parse(self):
        rules, _ = self.file(0)
        debugCssParser("parse:", rules)
        return rules
    
    def value(self, i):
        j = i
        while self.s[j].isalnum() or self.s[j] in "-.":
            j += 1
        debugCssParser("value:", self.s[i:j])
        return self.s[i:j], j
    
    def whitespace(self, i):
        j = i
        while j < len(self.s) and self.s[j].isspace():
            j += 1
        debugCssParser("whitespace: len", j - i)
        return None, j
    
    def pair(self, i):
        prop, i = self.value(i)
        _, i = self.whitespace(i)
        assert self.s[i] == ":"
        _, i = self.whitespace(i + 1)
        val, i = self.value(i)
        _, i = self.whitespace(i)
        debugCssParser("pair:", prop.lower(), val)
        return (prop.lower(), val), i
    
    def selector(self, i):
        if self.s[i] == "#":
            name, i = self.value(i+1)
            debugCssParser("IDSelector:", name)
            return IdSelector(name), i
        elif self.s[i] == ".":
            name, i = self.value(i+1)
            debugCssParser("ClassSelector:", name)
            return ClassSelector(name), i
        else:
            name, i = self.value(i)
            debugCssParser("TagSelector:", name)
            return TagSelector(name.lower()), i
    
    def body(self, i):
        pairs = {}
        if len(self.s) <= i:
            return pairs, i
        assert self.s[i] == "{"
        _, i = self.whitespace(i+1)
        while True:
            if i > len(self.s): break
            if self.s[i] == "}": break

            try:
                (prop, val), i = self.pair(i)
                pairs[prop] = val
                _, i = self.whitespace(i)
                assert self.s[i] == ";"
                _, i = self.whitespace(i+1)
            except AssertionError:
                debugCssParser("CSS Parse Error: key, value pair near", self.s[i-10:i+10])
                while self.s[i] not in [";", "}"]:
                    i += 1
                if self.s[i] == ";":
                    _, i = self.whitespace(i + 1)
        assert self.s[i] == "}"
        debugCssParser("body:", pairs)
        return pairs, i+1
    
    def rule(self, i):
        selector, i = self.selector(i)
        _, i = self.whitespace(i)
        body, i = self.body(i)
        debugCssParser("rule:", (selector, body))
        return (selector, body), i
    
    def file(self, i):
        rules = []
        _, i = self.whitespace(i)
        while i < len(self.s):
            try:
                rule, i = self.rule(i)
            except AssertionError:
                while i < len(self.s) and self.s[i] != "}":
                    i += 1
                i += 1
            else:
                rules.append(rule)
            _, i = self.whitespace(i)
        debugCssParser("file:", rules)
        return rules, i
