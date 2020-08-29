from src.util.socket_util import SOCKET_NEWLINE

# Parse the given response
# response: File
def parseHTTPResponse(response):

    # Status Line
    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    if status != "200":
        return status, {}, ""

    # Headers
    headers = {}
    while True:
        line = response.readline()
        if line == SOCKET_NEWLINE: break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()
    
    html = response.read()
    return status, headers, html