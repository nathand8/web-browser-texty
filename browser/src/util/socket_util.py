import socket, ssl

SOCKET_NEWLINE = "\r\n"
SOCKET_ENCODING = "utf8"

class EnhancedSocket:

    def __init__(self):
        self.s = socket.socket(
            family = socket.AF_INET,
            type = socket.SOCK_STREAM,
            proto = socket.IPPROTO_TCP
        )
    
    # Connect to given host on given port
    def connect(self, host, port, encrypted = False):
        if encrypted:
            ctx = ssl.create_default_context()
            self.s = ctx.wrap_socket(self.s, server_hostname=host)
        self.s.connect((host, port))

    # Close the soclet
    def close(self):
        self.s.close()

    # Takes a list of lines and sends them over the socket
    def sendLines(self, lines):
        self.s.send((SOCKET_NEWLINE.join(lines) + SOCKET_NEWLINE + SOCKET_NEWLINE).encode(SOCKET_ENCODING))
        return

    # Read from the socket to a file-like object
    def makefile(self):
        return self.s.makefile("r", encoding=SOCKET_ENCODING, newline=SOCKET_NEWLINE)

