#!/usr/bin/env python3
"""AI圆桌讨论服务器 - 支持文件读取"""

import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs

PORT = 8530
DIRECTORY = r"D:\aiwork"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # 文件列表API
        if parsed_path.path == '/list_files':
            params = parse_qs(parsed_path.query)
            folder_path = params.get('path', [DIRECTORY])[0]
            
            try:
                if os.path.isdir(folder_path):
                    files = []
                    for item in os.listdir(folder_path):
                        item_path = os.path.join(folder_path, item)
                        if os.path.isfile(item_path):
                            size = os.path.getsize(item_path)
                            # 只显示代码和文本文件
                            ext = os.path.splitext(item)[1].lower()
                            if ext in ['.py', '.js', '.json', '.wxss', '.wxml', '.wcss', '.ts', '.tsx', '.html', '.css', '.md', '.txt', '.vue'] or not ext:
                                files.append({
                                    'name': item,
                                    'path': item_path,
                                    'size': size
                                })
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'files': files}).encode())
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'files': [], 'error': '目录不存在'}).encode())
            except Exception as e:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'files': [], 'error': str(e)}).encode())
            return
        
        # 读取文件内容API
        if parsed_path.path == '/read_file':
            params = parse_qs(parsed_path.query)
            file_path = params.get('path', [''])[0]
            
            try:
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    # 限制内容大小
                    if len(content) > 5000:
                        content = content[:5000] + '\n\n... (内容过长已截断)'
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'content': content, 'name': os.path.basename(file_path)}).encode())
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': '文件不存在'}).encode())
            except Exception as e:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            return
        
        return super().do_GET()
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    print(f"启动服务器: http://localhost:{PORT}")
    print(f"按 Ctrl+C 停止")
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止")
