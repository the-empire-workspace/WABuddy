import http.server
import urllib.parse

class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        if "code" in query:
            code = query["code"][0]
            self.server.code = code
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<h1>Login exitoso. Puedes cerrar esta ventana.</h1>")
        else:
            self.send_error(400, "No se recibió el código.")
