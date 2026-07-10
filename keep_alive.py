from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"VINZ CPANEL BOT IS ONLINE!")

def run_server():
    # Menggunakan port 8080 (pastikan port ini ter-bind di network panel Ptero kamu)
    # Jika panel Ptero kamu mengalokasikan port lain, ubah 8080 ke port tersebut
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()

def keep_alive():
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()
