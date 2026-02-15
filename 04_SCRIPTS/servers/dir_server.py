#!/usr/bin/env python3
"""
Custom directory server with a styled index (glassy + flame/cyan theme).
Usage: python3 dir_server.py [port] [directory]
Defaults: port=4500, directory=/home/saba
"""
import http.server
import os
import sys
import urllib
from datetime import datetime

class PrettyHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            entries = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        entries.sort(key=lambda a: a.lower())
        displaypath = urllib.parse.unquote(self.path)
        r = []
        enc = sys.getfilesystemencoding()

        r.append("<!DOCTYPE html><html><head>")
        r.append('<meta charset="utf-8">')
        r.append("<title>🜂 VES Index</title>")
        r.append(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Inter:wght@400;600&display=swap');
            :root { --bg:#05060a; --glass:rgba(255,255,255,0.04); --border:rgba(0,216,224,0.35); --flame:#f46000; --cyan:#00d8e0; --text:#f0f0f0; }
            *{box-sizing:border-box;}
            body{margin:0;padding:30px;font-family:'Inter',sans-serif;background:radial-gradient(circle at 20% 20%, rgba(244,96,0,0.16), transparent 30%),radial-gradient(circle at 80% 30%, rgba(0,216,224,0.16), transparent 35%),#05060a;color:var(--text);}
            h1{margin:0 0 12px 0;font-family:'Cinzel',serif;color:var(--cyan);letter-spacing:0.03em;}
            .card{background:var(--glass);backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:14px;box-shadow:0 18px 60px rgba(0,0,0,0.45);padding:18px 20px;}
            table{width:100%;border-collapse:collapse;margin-top:10px;}
            th,td{text-align:left;padding:10px 8px;}
            th{color:var(--cyan);border-bottom:1px solid rgba(255,255,255,0.1);font-size:0.9rem;}
            tr:hover td{background:rgba(255,255,255,0.04);}
            a{color:var(--text);text-decoration:none;}
            a:hover{color:var(--flame);}
            .pill{display:inline-block;padding:4px 8px;border-radius:8px;font-size:0.78rem;border:1px solid var(--border);color:var(--cyan);}
            .path{color:#9aa3b0;font-size:0.9rem;margin-bottom:8px;}
            .footer{margin-top:10px;font-size:0.85rem;color:#9aa3b0;}
            </style>
            """
        )
        r.append("</head><body>")
        r.append('<div class="card">')
        r.append("<h1>🜂 VES Index</h1>")
        r.append(f'<div class="path">{displaypath}</div>')
        r.append('<table aria-label="Directory listing"><tr><th>Name</th><th>Size</th><th>Modified</th></tr>')

        # Parent link
        if displaypath != "/":
            parent = urllib.parse.quote(os.path.join(displaypath, ".."))
            r.append(f'<tr><td><a href="{parent}">..</a></td><td>—</td><td>—</td></tr>')

        for name in entries:
            fullname = os.path.join(path, name)
            display_name = link_name = name
            if os.path.isdir(fullname):
                display_name = name + "/"
                link_name = name + "/"
            elif os.path.islink(fullname):
                display_name = name + "@"

            encoded = urllib.parse.quote(link_name)
            size = "—"
            mtime = "—"
            try:
                st = os.stat(fullname)
                size = f"{st.st_size/1024:.1f} KB" if st.st_size < 1024*1024 else f"{st.st_size/1024/1024:.2f} MB"
                mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
            except OSError:
                pass

            r.append(f'<tr><td><a href="{encoded}">{display_name}</a></td><td>{size}</td><td>{mtime}</td></tr>')

        r.append("</table>")
        r.append('<div class="footer">Sidro stoji • Plamen gori</div>')
        r.append("</div></body></html>")

        encoded = "\n".join(r).encode(enc, "surrogateescape")
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return io.BytesIO(encoded)


if __name__ == "__main__":
    import io
    from functools import partial

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4500
    directory = sys.argv[2] if len(sys.argv) > 2 else "/home/saba"
    os.chdir(directory)
    handler = partial(PrettyHandler, directory=directory)
    with http.server.ThreadingHTTPServer(("0.0.0.0", port), handler) as httpd:
        print(f"🜂 Serving {directory} on http://0.0.0.0:{port} with pretty index")
        httpd.serve_forever()
