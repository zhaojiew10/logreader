import http.server
import socketserver
import os
import mimetypes
import gzip

class LogreaderHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):


    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = directory
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        file_path = self.translate_path(self.path)
        print(file_path)
        f = self.send_head()
        if f:
            try:
                if file_path.endswith('.gz'):
                    self.extract_gz_file(file_path,self.wfile)
                else:
                    self.copyfile(f, self.wfile)
            finally:
                f.close()

    def extract_gz_file(self, file_path, f_out):
            with gzip.open(file_path, 'rb') as f_in:
                self.copyfile(f_in, f_out)
                
    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default,
        '.gz': 'text/plain',
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })

Handler = LogreaderHTTPRequestHandler

PORT = 8000

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()