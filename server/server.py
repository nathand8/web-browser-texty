import socket
import sys
import random

TOKENS = {}
NONCES = {}

def handle_connection(conx):
    # Read the Opening Lines
    req = conx.makefile("rb")
    reqline = req.readline().decode('utf8')
    method, url, version = reqline.split(" ", 2)
    assert method in ["GET", "POST"]

    # Read the headers
    headers = {}
    for line in req:
        line = line.decode('utf8')
        if line == '\r\n': break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()

    # Read the Body (If it exists)
    if 'content-length' in headers:
        length = int(headers['content-length'])
        body = req.read(length).decode('utf8')
    else:
        body = None

    # Handle the Request
    body, headers = handle_request(method, url, headers, body)

    # Send the response
    response = "HTTP/1.0 200 OK\r\n"
    response += "Content-Length: {}\r\n".format(len(body.encode("utf8")))
    for header, value in headers.items():
        response += "{}: {}\r\n".format(header, value)
    response += "\r\n" + body
    conx.send(response.encode('utf8'))
    conx.close()


LOGINS = { "bob": "123", "jon": "qwe" }

def check_login(username, pw):
    return username in LOGINS and LOGINS[username] == pw

def parse_cookies(s):
    out = {}
    for cookie in s.split(";"):
        if "=" in cookie:
            k, v = cookie.strip().split("=", 1)
            out[k] = v
    return out

ENTRIES = [
    ('Pavel was here', 'bob'),
    ('Until next time', 'jon'),
]

def show_comments(username):

    out = """
    <!doctype html><html>
    <script src=/comment.js></script>
    <link rel=stylesheet href=/comment.css>"""
    if username:
        nonce = str(random.random())[2:]
        NONCES[username] = nonce
        out += """
        <form action=add method=post>
            <p>Message:<input name=guest></p>
            <p><button>Sign the book!</button></p>"""
        out += "<p><input name=nonce type=hidden value=" + nonce + "></p>"

        out += "</form>"
    else:
        out += "<p><a href=/login>Log in to add to the guest list</a></p>"

    out += "<p id=errors></p>"
    out += "<p><a href=/clear>Clear Guestbook</a></p>"

    for entry, who in ENTRIES:
        if not who:
            who = "unknown"
        if not entry:
            entry = "missing entry"

        # Escape the user input
        entry = entry.replace("&", "&amp;").replace("<", "&lt;")
        out += '<p>' + entry + " <i>from " + who + '</i></p>'
    return out


def add_entry(params, username):
    if 'nonce' not in params or params['nonce'] != NONCES.get(username):
        return "Invalid nonce"
    if 'guest' in params and len(params['guest']) <= 200:
        ENTRIES.append((params['guest'], username))
    return show_comments(username)


def handle_request(method, url, headers, body):
    resp_headers = {}
    out = ""
    username = None
    if "cookie" in headers:
        token = parse_cookies(headers["cookie"]).get("token")
        username = TOKENS.get(token)
    
    if method == "POST":
        params = form_decode(body)
        if url == "/":
            if check_login(params.get("username"), params.get("password")):
                username = params["username"]
                token = str(random.random())[2:]
                TOKENS[token] = username
                resp_headers["Set-Cookie"] = "token=" + token
            out = show_comments(username)
        elif url == '/add':
            out = add_entry(params, username)
        else:
            out = show_comments(username)
    else:
        if url == "/clear":
            print("Clearing the guestbook entries")
            ENTRIES.clear()
            out = show_comments(username)
        if url == "/login":
            with open("login.html") as f:
                out = f.read()
        elif url == "/comment.js":
            with open("comment.js") as f:
                out = f.read()
        elif url == "/comment.css":
            with open("comment.css") as f:
                out = f.read()
        else:
            out = show_comments(username)
    return out, resp_headers


def form_decode(body):
    params = {}
    for field in body.split("&"):
        name, value = field.split("=", 1)
        params[name] = value.replace("%20", " ")
    return params

if __name__ == "__main__":
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    s.bind(('', port))
    s.listen()

    while True:
        conx, addr = s.accept()
        handle_connection(conx)