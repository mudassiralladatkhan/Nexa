#!/usr/bin/env python3
"""
Simple HTTP Server for Nexa Frontend
Alternative server on port 3001 if 3000 is busy
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Change to frontend directory
frontend_dir = Path(__file__).parent
os.chdir(frontend_dir)

# Try different ports
PORTS = [3000, 3001, 3002, 8080]

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    for port in PORTS:
        try:
            with socketserver.TCPServer(("", port), SimpleHandler) as httpd:
                print(f"🌐 Nexa Frontend Server Started!")
                print(f"📡 URL: http://localhost:{port}")
                print(f"📱 App: http://localhost:{port}/index.html")
                print(f"🧪 Test: http://localhost:{port}/test.html")
                print(f"💡 Press Ctrl+C to stop")
                print("-" * 50)
                
                # Open browser
                webbrowser.open(f'http://localhost:{port}')
                
                httpd.serve_forever()
                
        except OSError as e:
            if "Address already in use" in str(e) or "10048" in str(e):
                print(f"Port {port} is busy, trying next port...")
                continue
            else:
                print(f"Error on port {port}: {e}")
                continue
    
    print("❌ All ports are busy. Please stop other servers and try again.")
    sys.exit(1)

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
