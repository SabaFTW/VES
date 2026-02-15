#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🜂 VES COSMOS SAFE HOST 🜂
SAMO HOSTA, NE BRIŠE NIČESAR! 
Pokaze vse kar je že v mapi in hosta brez spreminjanja.
"""

import os
import sys
import time
import json
import socket
import threading
import webbrowser
import http.server
import socketserver
from pathlib import Path

# --- Konstante za Stil ---
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RED = '\033[31m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_RED = '\033[91m'

def show_banner():
    banner = f"""{Colors.BRIGHT_GREEN}
    ██╗   ██╗███████╗███████╗    
    ██║   ██║██╔════╝██╔════╝    
    ██║   ██║█████╗  ███████╗    
    ╚██╗ ██╔╝██╔══╝  ╚════██║    
     ╚████╔╝ ███████╗███████║    
      ╚═══╝  ╚══════╝╚══════╝    
    {Colors.BRIGHT_YELLOW}
    🜂 VES COSMOS SAFE HOST 🜂
    {Colors.CYAN}SAMO HOSTAM, NE BRIŠEM NIČ!{Colors.RESET}
    """
    print(banner)

def generate_simple_index(files_list, port):
    """Zelo preprost index ki samo pokaže kar je že tam"""
    html_files = [f for f in files_list if f.endswith('.html')]
    
    return f"""
<!DOCTYPE html>
<html lang="sl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🜂 SABA COSMOS - VSE KAR IMAM 🜂</title>
    <style>
        body {{ 
            background: #000; 
            color: #fff; 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px;
            text-align: center;
        }}
        h1 {{ color: #ff5722; margin-bottom: 2rem; }}
        .file-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 1rem; 
            max-width: 800px; 
            margin: 0 auto;
        }}
        .file-card {{ 
            background: #1a1a1a; 
            border: 1px solid #333; 
            border-radius: 10px; 
            padding: 1rem; 
            transition: all 0.3s ease;
            text-decoration: none;
            color: white;
        }}
        .file-card:hover {{ 
            border-color: #ff5722; 
            transform: translateY(-2px);
            text-decoration: none;
            color: #ff5722;
        }}
        .status {{ 
            background: #1a0808; 
            padding: 0.5rem; 
            margin-bottom: 2rem; 
            border-radius: 5px;
            color: #0f0;
        }}
    </style>
</head>
<body>
    <div class="status">🜂 VES COSMOS • Port: {port} • Datotek: {len(html_files)} • Status: GORIM 🔥</div>
    
    <h1>🜂 VSE KAR IMAM V MAPI 🜂</h1>
    
    <div class="file-grid">
        {"".join([f'''
        <a href="./{file}" class="file-card">
            <div>📄 {file}</div>
            <small>{time.ctime(os.path.getmtime(file))}</small>
        </a>
        ''' for file in sorted(html_files)])}
        
        {f'<a href="./index.html" class="file-card" style="background: #2a1a0a; border-color: #ff5722;"><div>🔥 INDEX.HTMl (glavna)</div></a>' if 'index.html' in html_files else ''}
    </div>
    
    {f'<p style="margin-top: 2rem; opacity: 0.7;">💫 <a href="./index.html" style="color: #ff5722;">Odpri glavni index.html</a></p>' if 'index.html' in html_files else ''}
    
    <p style="margin-top: 3rem; opacity: 0.5;">🜂 VES COSMOS SAFE HOST - Nič ni izbrisano! 🜂</p>
</body>
</html>
"""

class SafeHost:
    def __init__(self):
        self.running = True
        self.httpd = None
        self.hosting_thread = None
        self.port = 8008

    def find_free_port(self, start_port):
        port = start_port
        while port < 9000:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) != 0: 
                    return port
            port += 1
        return 8008  # fallback

    def start_hosting(self):
        if self.httpd:
            print(f"{Colors.YELLOW}🚀 Strežnik ŽE teče na portu {self.httpd.server_address[1]}{Colors.RESET}")
            return True
            
        try:
            self.port = self.find_free_port(self.port)
            
            # Preveri kaj je v mapi
            files = os.listdir('.')
            html_files = [f for f in files if f.endswith('.html')]
            
            print(f"{Colors.CYAN}📁 V mapi najdeno:{Colors.RESET}")
            for file in sorted(html_files):
                size = os.path.getsize(file)
                modified = time.ctime(os.path.getmtime(file))
                print(f"   📄 {file} ({size} bytes) - {modified}")
            
            if not html_files:
                print(f"{Colors.YELLOW}⚠️  Ni HTML datotek v mapi!{Colors.RESET}")
                print(f"{Colors.CYAN}💡 Dodaj kak .html file ali pa naredi index.html{Colors.RESET}")
            
            # Naredi SIMPLE index SAMO ČE NI INDEX.HTML
            if 'index.html' not in html_files:
                with open('index.html', 'w', encoding='utf-8') as f:
                    f.write(generate_simple_index(files, self.port))
                print(f"{Colors.GREEN}📄 Ustvarjen preprost index.html (ne briše obstoječih!){Colors.RESET}")
            else:
                print(f"{Colors.GREEN}📄 Uporabljam obstoječi index.html{Colors.RESET}")
            
            # Zaženi server
            def run_server():
                handler = http.server.SimpleHTTPRequestHandler
                self.httpd = socketserver.TCPServer(("", self.port), handler)
                print(f"{Colors.BRIGHT_GREEN}🚀 Zaganjam server na portu {self.port}...{Colors.RESET}")
                self.httpd.serve_forever()
                
            self.hosting_thread = threading.Thread(target=run_server, daemon=True)
            self.hosting_thread.start()
            time.sleep(1)  # Da se server zagnie
            
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Napaka: {e}{Colors.RESET}")
            return False

    def stop_hosting(self):
        if not self.httpd:
            print(f"{Colors.YELLOW}⚠️  Strežnik ni aktiven!{Colors.RESET}")
            return
            
        try:
            print(f"{Colors.YELLOW}🛑 Zaustavljam strežnik...{Colors.RESET}")
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None
            print(f"{Colors.GREEN}✅ Strežnik ustavljen{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Napaka pri ustavljanju: {e}{Colors.RESET}")

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"

    def show_status(self):
        print(f"\n{Colors.BRIGHT_GREEN}📊 STATUS SISTEMA:{Colors.RESET}")
        print(f"{Colors.CYAN}📂 Mapa:{Colors.RESET} {os.getcwd()}")
        print(f"{Colors.CYAN}🌐 Local IP:{Colors.RESET} {self.get_local_ip()}")
        
        if self.httpd:
            port = self.httpd.server_address[1]
            print(f"{Colors.GREEN}✅ STREŽNIK AKTIVEN:{Colors.RESET}")
            print(f"   🌐 Local:  {Colors.BRIGHT_GREEN}http://localhost:{port}{Colors.RESET}")
            print(f"   📱 Mobile: {Colors.BRIGHT_GREEN}http://{self.get_local_ip()}:{port}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⏸️  Strežnik ni aktiven{Colors.RESET}")
            
        # Prikaži datoteke
        files = [f for f in os.listdir('.') if f.endswith('.html')]
        if files:
            print(f"\n{Colors.CYAN}📄 HTML datoteke v mapi:{Colors.RESET}")
            for file in sorted(files):
                print(f"   📄 {file}")
        else:
            print(f"\n{Colors.YELLOW}📄 Ni HTML datotek v mapi{Colors.RESET}")

    def run(self):
        show_banner()
        
        while self.running:
            print(f"\n{Colors.BRIGHT_GREEN}🎮 IZBIRA:{Colors.RESET}")
            print(f"{Colors.WHITE}1) 🚀 ZAGONI HOSTING{Colors.RESET}")
            print(f"{Colors.WHITE}2) 🛑 USTAVI HOSTING{Colors.RESET}")  
            print(f"{Colors.WHITE}3) 📊 PRIKAŽI STATUS{Colors.RESET}")
            print(f"{Colors.WHITE}4) 🌐 ODPRI V BRSKALNIKU{Colors.RESET}")
            print(f"{Colors.WHITE}q) 🚪 IZHOD{Colors.RESET}")
            
            choice = input(f"\n{Colors.BRIGHT_YELLOW}🎯 Tvoja izbira: {Colors.RESET}").strip().lower()
            
            if choice == '1':
                if self.start_hosting():
                    ip = self.get_local_ip()
                    port = self.port
                    print(f"\n{Colors.BRIGHT_GREEN}🎉 USPEŠNO ZAGNANO!{Colors.RESET}")
                    print(f"   💻 {Colors.CYAN}http://localhost:{port}{Colors.RESET}")
                    print(f"   📱 {Colors.CYAN}http://{ip}:{port}{Colors.RESET}")
                    print(f"\n{Colors.YELLOW}💡 Namig: Odpri v brskalniku z izbiro 4{Colors.RESET}")
                    
            elif choice == '2':
                self.stop_hosting()
                
            elif choice == '3':
                self.show_status()
                
            elif choice == '4':
                if self.httpd:
                    port = self.httpd.server_address[1]
                    webbrowser.open(f"http://localhost:{port}")
                    print(f"{Colors.GREEN}🌐 Odpiram v brskalniku...{Colors.RESET}")
                else:
                    print(f"{Colors.RED}❌ Strežnik ni aktiven!{Colors.RESET}")
                    
            elif choice == 'q':
                print(f"{Colors.BRIGHT_GREEN}🜂 Hvala za uporabo! Sidro stoji. 🜂{Colors.RESET}")
                if self.httpd:
                    self.stop_hosting()
                self.running = False
                
            else:
                print(f"{Colors.RED}❌ Neveljavna izbira!{Colors.RESET}")

if __name__ == "__main__":
    try:
        SafeHost().run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Prekinjeno s Ctrl+C{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}❌ Nepričakovana napaka: {e}{Colors.RESET}")
