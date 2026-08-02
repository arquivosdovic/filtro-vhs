#!/usr/bin/env python3
"""
Servidor local simples que adiciona os cabeçalhos necessários para
habilitar SharedArrayBuffer (necessário para o ffmpeg.wasm funcionar).

Uso:
    python3 servidor.py

Depois abra: http://localhost:8000/vhs-video.html
"""
import http.server
import socketserver

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servindo em http://localhost:{PORT} (com headers COOP/COEP)")
    httpd.serve_forever()
