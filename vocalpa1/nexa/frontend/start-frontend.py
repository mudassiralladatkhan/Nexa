#!/usr/bin/env python3
"""
Nexa Frontend - Simple HTTP Server
Serves the web PWA frontend
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

PORT = 3000

class NexaHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for Nexa frontend"""
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    print("🌐 Starting Nexa Frontend Server...")
    print("=" * 50)
    print(f"📡 Server URL: http://localhost:{PORT}")
    print(f"📱 PWA App: http://localhost:{PORT}/index.html")
    print(f"📚 Manifest: http://localhost:{PORT}/manifest.json")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), NexaHTTPRequestHandler) as httpd:
            print(f"✅ Serving Nexa Frontend at http://localhost:{PORT}")
            
            # Open browser after a short delay
            import threading
            def open_browser():
                import time
                time.sleep(2)
                webbrowser.open(f'http://localhost:{PORT}')
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Shutting down Nexa frontend...")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
