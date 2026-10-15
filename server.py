"""
Vortex YouTube Shorts Studio - Local Web Server
Provides Web GUI to preview, render, and upload videos with 1-click.
"""

import os
import sys
import json
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Ensure root package resolution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_pipeline import run_pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

class StudioHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.do_GET(head_only=True)

    def do_GET(self, head_only=False):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(WEB_DIR, "index.html"), "rb") as f:
                self.wfile.write(f.read())
            return

        elif path == "/render":
            params = parse_qs(parsed.query)
            topic = params.get("topic", ["y2k38_bug"])[0]
            voice = params.get("voice", ["hi_male"])[0]
            output_name = f"{topic}_latest.mp4"

            try:
                result = run_pipeline(
                    topic_id=topic,
                    voice_key=voice,
                    output_filename=output_name
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "SUCCESS",
                    "video": f"/output/{output_name}",
                    "details": result
                }).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ERROR", "error": str(e)}).encode("utf-8"))
            return

        elif path == "/video":
            # Find the most recently modified MP4 in output
            mp4_files = [
                os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR)
                if f.endswith(".mp4") and not f.endswith("_bg.mp4")
            ]
            if not mp4_files:
                # fallback to any mp4
                mp4_files = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.endswith(".mp4")]

            if not mp4_files:
                self.send_response(404)
                self.end_headers()
                return

            latest_mp4 = max(mp4_files, key=os.path.getmtime)
            file_size = os.path.getsize(latest_mp4)

            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Content-Length", str(file_size))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()

            if not head_only:
                with open(latest_mp4, "rb") as f:
                    self.wfile.write(f.read())
            return

        else:
            self.send_response(404)
            self.end_headers()

def start_server(port: int = 8080):
    server = HTTPServer(("127.0.0.1", port), StudioHandler)
    print(f"\n🚀 Vortex Shorts Studio Web Server running at: http://localhost:{port}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()

if __name__ == "__main__":
    start_server(8080)
