import logging
import os
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler

logger = logging.getLogger(__name__)

class MyServer(SimpleHTTPRequestHandler):
    index_page = ""
    home = ""
    def do_GET(self):
        global html
        global home

        if self.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(self.index_page, "utf-8"))
        elif self.path.find(".html") != -1:
            logger.warning("%s/%s", self.home, self.path)

            try:
                f = open(os.path.join(self.home, os.path.basename(self.path)), 'r')

                ctype = self.guess_type(self.path)
                fs = os.fstat(f.fileno())
                self.send_response(200)
                self.send_header("Content-type", ctype)
                self.send_header("Content-Length", str(fs[6]))
                self.end_headers()            
                
                self.wfile.write(bytes(f.read(), "utf-8"))
            except OSError as e:
                logger.warning("home is %s", self.home)
                logger.exception(e)
                self.send_response(HTTPStatus.NOT_FOUND, "file not found")
                return None
            
        elif self.path.find(".png") != -1:
            logger.info("%s", self.path)

            try:
                f = open(os.path.join(self.home, os.path.basename(self.path)), 'rb')

                ctype = self.guess_type(self.path)
                fs = os.fstat(f.fileno())
                self.send_response(200)
                self.send_header("Content-type", ctype)
                self.send_header("Content-Length", str(fs[6]))
                self.end_headers()            
                
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()
            except OSError as e:
                self.send_response(HTTPStatus.NOT_FOUND, "file not found")
                return None


def serve_images_files(root_dir: str, paths: list[str], port: int=8080):
    MyServer.home = root_dir

    pre = "<html><head></head><body>"
    post = "</body></hmtl"

    body = []
    for path in paths:
        file = os.path.basename(path)
        body.append("<div style='border: 1px silver solid;text-align:center;width:500px;margin:20px auto'>")
        body.append(f"<img src='{path}' style='width:100%' alt='{file}'></img>")
        body.append("</div>")

    MyServer.index_page = pre + "\n".join(body) + post

    logger.info("serving images files at %s", port)
    server = HTTPServer(('', port), MyServer)
    server.serve_forever()

