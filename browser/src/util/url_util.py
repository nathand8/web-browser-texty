# This should take a url and split it into the protocol, host, and path
def splitURL(url):
    protocol, url = url.split("://", 1)
    assert protocol == "http", "Unknown protocol: %s" % protocol
    host, path = url.split("/", 1)
    path = "/" + path
    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
    else:
        port = 80
    return protocol, host, port, path
