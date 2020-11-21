import socket

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
    body = handle_request(method, url, headers, body)

    # Send the response
    response = "HTTP/1.0 200 OK\r\n"
    response += "Content-Length: {}\r\n".format(len(body.encode("utf8")))
    response += "\r\n" + body
    conx.send(response.encode('utf8'))
    conx.close()


ENTRIES = [ 'Pavel was here' ]

def show_comments():
    with open("comment.html") as f:
        out = f.read()

    for entry in ENTRIES:
        out += "<p>" + entry + "</p>"
    return out


def add_entry(params):
    if 'guest' in params and len(params['guest']) <= 100:
        ENTRIES.append(params['guest'])
    return show_comments()


def handle_request(method, url, headers, body):
    if method == 'POST':
        params = form_decode(body)
        if url == '/add':
            return add_entry(params)
        else:
            return show_comments()
    else:
        if url == "/comment.js":
            with open("comment.js") as f:
                return f.read()
        if url == "/comment.css":
            with open("comment.css") as f:
                return f.read()
        return show_comments()


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

    s.bind(('', 8000))
    s.listen()

    while True:
        conx, addr = s.accept()
        handle_connection(conx)