#!/usr/bin/env python3
import http.server
import socketserver
import os

# Change to the directory containing the HTML file
os.chdir('/Users/bhagya/Desktop/chatbot')

PORT = 3000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🌐 Frontend server running at http://localhost:{PORT}")
    print(f"📱 Open http://localhost:{PORT}/frontend.html in your browser")
    print("Press Ctrl+C to stop the server")
    httpd.serve_forever()
