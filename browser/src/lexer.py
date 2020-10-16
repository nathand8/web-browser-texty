class Text:
    def __init__(self, text):
        self.text = text

class Tag:
    def __init__(self, text):
        parts = text.split()
        self.tag = parts[0].lower()
        self.attributes = {}
        for attrpair in parts[1:]:
            if "=" in attrpair:
                key, value = attrpair.split("=", 1)
                if len(value) > 2 and value[0] in ["'", "\""]:
                    value = value[1:-1]
                self.attributes[key.lower()] = value
            else:
                self.attributes[attrpair.lower()] = ""
    
    def __repr__(self):
        return "<" + self.tag + " " + str(self.attributes) + ">"

def lex(body):
    # return stripTags(body)
    out = []
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if text: out.append(Text(text))
            text = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(text))
            text = ""
        else:
            text += c
    if not in_tag and text:
        out.append(Text(text))
    return out