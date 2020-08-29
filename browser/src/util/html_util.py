# Return equivalent HTML with all tags removed
def stripTags(raw_html):
    html_sans_tags = ""
    in_angle = False
    for c in raw_html:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            html_sans_tags += c
    return html_sans_tags
