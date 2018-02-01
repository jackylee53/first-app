import BaseHTTPServer
import cgi, random, sys,re
from lib.configuration import Config_reader

class Handler(object,BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "file not found");
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        try:
            stdout = sys.stdout
            sys.stdout = self.wfile
            self.makepage()
        finally:
            sys.stdout = stdout

    def makepage(self):
        log_path = Config_reader().get_value(section='LOGGER',key='LOG_PATH')
        f=open(log_path,'rb')
        line = f.readlines()
        print "<html><title>whitelist</title><body>"
        for i in line:
            if not re.match('.*DEBUG.*',i):
                print '<br>%s</br>'%cgi.escape(i)
        print "</body></html>"

    def main(self):
        PORT = 8000
        httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
        print "serving at port", PORT
        httpd.serve_forever()

