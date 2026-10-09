#!/usr/bin/env python3
"""
Minimal local HTTP (not HTTPS) login form, built for Lab 2 Exercise C.

Purpose: demonstrate -- on a server you own, on your own machine, with
fake credentials -- that plain HTTP submits form data in cleartext,
which Wireshark can read directly off the wire. Never point this
technique at a server or form you don't own or have explicit
permission to test.

Usage:
    python3 http_login_demo.py
    Then open http://localhost:8080 in a browser and submit the form.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

PORT = 8080

LOGIN_FORM = b"""<!DOCTYPE html>
<html>
<head><title>Test Login (HTTP, not HTTPS)</title></head>
<body>
  <h1>Test Login Form -- Plain HTTP</h1>
  <p>This form is intentionally served over HTTP, not HTTPS, for Lab 2
     Exercise C. Do not enter real credentials.</p>
  <form method="POST" action="/login">
    <label>Username: <input type="text" name="username" value="testuser"></label><br><br>
    <label>Password: <input type="password" name="password" value="SuperSecret123"></label><br><br>
    <input type="submit" value="Log In">
  </form>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(LOGIN_FORM)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        fields = parse_qs(body)
        print(f"[http_login_demo] Received POST body: {body}")
        print(f"[http_login_demo] Parsed fields: {fields}")

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(
            b"<html><body><h1>Login submitted (plaintext, over HTTP)</h1>"
            b"<p>Check Wireshark -- this request was not encrypted.</p>"
            b"</body></html>"
        )

    def log_message(self, format, *args):
        pass  # keep terminal output limited to our own prints above

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Serving test login form at http://localhost:{PORT}  (Ctrl+C to stop)")
    server.serve_forever()
