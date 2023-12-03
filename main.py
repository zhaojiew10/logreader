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
    
    # Override parent method to change content-length
    def end_headers(self):
        if self.request_version != 'HTTP/0.9':
            self._headers_buffer.append(b"\r\n")
            print("not flush header")
        
    def do_GET(self):
        file_path = self.translate_path(self.path)
        # print("Check log of *===============", file_path, "*=====================")
        f = self.send_head()
        
        if f:
            try:
                if file_path.endswith('.gz'):
                    self.extract_gz_file(file_path,self.wfile)
                else:
                    self.flush_headers()
                    self.copyfile(f, self.wfile)
            except Exception as e:
                print(e)
            finally:
                f.close()

    def extract_gz_file(self, file_path, f_out):
        with gzip.open(file_path, 'rb') as f_in:
            self.send_header("Content-Length", len(f_in.read()))
            # Remove the header content-length from the headers buffer
            self._headers_buffer.pop(4)
            # Flush the headers
            self.flush_headers()
            # Reset the file pointer
            f_in.seek(0)
            # Copy the file
            self.copyfile(f_in, f_out)
                
    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
        
    extensions_map = mimetypes.types_map.copy()
    
    
    # Update the extensions_map dictionary with the given key gzip
    extensions_map.update({
        '': 'application/octet-stream', # Default,
        '.gz': 'text/plain',
        '.py': 'text/plain',
        '.txt': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })
    
Handler = LogreaderHTTPRequestHandler

PORT = 8000

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()