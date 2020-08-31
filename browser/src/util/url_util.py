# This should take a url and split it into the scheme, host, and path
def splitURL(url):
    scheme, url = url.split("://", 1)
    assert scheme in ["http", "https"], "Unknown scheme: %s" % scheme
    host, path = url.split("/", 1)
    path = "/" + path
    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
    else:
        port = 80 if scheme == "http" else 443
    return scheme, host, port, path
