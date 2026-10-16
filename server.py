"""
Vortex YouTube Shorts Studio - Hardened Local Web Server
Asynchronous non-blocking architecture, input validation, chunked streaming, and job status tracking.
"""

import os
import sys
import json
import uuid
import logging
import threading
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any

# Ensure root package resolution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_pipeline import run_pipeline
from core.uploader import YouTubePublisher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Configure structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("VortexServer")

# Input Allowlisting
ALLOWED_TOPICS = {"y2k38_bug", "undersea_cables", "stuxnet_virus", "custom"}
ALLOWED_VOICES = {"hi_male", "hi_female", "en_male", "en_female", "en_us_male"}
ALLOWED_PRIVACY = {"private", "unlisted", "public"}

# Job State Store
JOBS: Dict[str, Dict[str, Any]] = {}
JOBS_LOCK = threading.Lock()

def async_render_worker(job_id: str, topic: str, voice: str):
    """Executes video generation in a background thread without blocking the HTTP server."""
    with JOBS_LOCK:
        JOBS[job_id]["status"] = "rendering"

    output_filename = f"{topic}_{job_id[:8]}.mp4"
    try:
        logger.info(f"Starting background render for job {job_id} (topic: {topic}, voice: {voice})")
        result = run_pipeline(
            topic_id=topic,
            voice_key=voice,
            output_filename=output_filename,
            auto_upload=False
        )
        with JOBS_LOCK:
            JOBS[job_id]["status"] = "completed"
            JOBS[job_id]["video_path"] = result["video_path"]
            JOBS[job_id]["video_url"] = f"/video?file={output_filename}"
            JOBS[job_id]["duration"] = result["duration"]
            JOBS[job_id]["size_mb"] = result["size_mb"]
        logger.info(f"Job {job_id} successfully completed.")
    except Exception as e:
        logger.error(f"Render failed for job {job_id}: {str(e)}", exc_info=True)
        with JOBS_LOCK:
            JOBS[job_id]["status"] = "failed"
            JOBS[job_id]["error"] = "Video generation encountered an error during processing. Check server logs."

class StudioHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Delegate HTTP logging to standard logger
        logger.debug(format % args)

    def _send_json(self, status_code: int, data: Dict[str, Any]):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_HEAD(self):
        self.do_GET(head_only=True)

    def do_GET(self, head_only=False):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            if not head_only:
                with open(os.path.join(WEB_DIR, "index.html"), "rb") as f:
                    self.wfile.write(f.read())
            return

        elif path == "/api/job-status":
            params = parse_qs(parsed.query)
            job_id = params.get("job_id", [None])[0]
            if not job_id:
                self._send_json(400, {"status": "ERROR", "message": "Missing 'job_id' parameter."})
                return

            with JOBS_LOCK:
                job_data = JOBS.get(job_id)

            if not job_data:
                self._send_json(404, {"status": "ERROR", "message": "Job ID not found."})
                return

            self._send_json(200, job_data)
            return

        elif path == "/video":
            params = parse_qs(parsed.query)
            target_filename = params.get("file", [None])[0]

            if target_filename:
                # Sanitize path to prevent directory traversal
                safe_name = os.path.basename(target_filename)
                target_path = os.path.join(OUTPUT_DIR, safe_name)
            else:
                # Find most recent completed short
                mp4_files = [
                    os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR)
                    if f.endswith(".mp4") and not f.endswith("_bg.mp4")
                ]
                target_path = max(mp4_files, key=os.path.getmtime) if mp4_files else None

            if not target_path or not os.path.exists(target_path):
                self.send_response(404)
                self.end_headers()
                return

            file_size = os.path.getsize(target_path)
            
            # Support HTTP Range requests for video seeking
            range_header = self.headers.get("Range")
            if range_header:
                byte_start, byte_end = 0, file_size - 1
                try:
                    parts = range_header.replace("bytes=", "").split("-")
                    if parts[0]:
                        byte_start = int(parts[0])
                    if len(parts) > 1 and parts[1]:
                        byte_end = int(parts[1])
                except ValueError:
                    pass

                byte_start = max(0, min(byte_start, file_size - 1))
                byte_end = max(byte_start, min(byte_end, file_size - 1))
                content_length = (byte_end - byte_start) + 1

                self.send_response(206)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Content-Range", f"bytes {byte_start}-{byte_end}/{file_size}")
                self.send_header("Content-Length", str(content_length))
                self.send_header("Accept-Ranges", "bytes")
                self.end_headers()

                if not head_only:
                    with open(target_path, "rb") as f:
                        f.seek(byte_start)
                        bytes_left = content_length
                        while bytes_left > 0:
                            chunk_size = min(65536, bytes_left)
                            data = f.read(chunk_size)
                            if not data:
                                break
                            self.wfile.write(data)
                            bytes_left -= len(data)
                return

            # Standard 200 OK stream (chunked delivery without buffering entire file in memory)
            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Content-Length", str(file_size))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()

            if not head_only:
                with open(target_path, "rb") as f:
                    while True:
                        chunk = f.read(65536)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
            return

        elif path == "/render":
            # Direct GET /render is deprecated for safety; instruct client to use POST
            self._send_json(405, {
                "status": "ERROR",
                "message": "Direct GET /render is disabled. Please use POST /api/render to initiate generation."
            })
            return

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/render":
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 32768:
                self._send_json(413, {"status": "ERROR", "message": "Request body too large."})
                return

            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8")) if body else {}
            except json.JSONDecodeError:
                self._send_json(400, {"status": "ERROR", "message": "Malformed JSON payload."})
                return

            topic = data.get("topic", "y2k38_bug")
            voice = data.get("voice", "hi_male")

            # Input validation against allowlists
            if topic not in ALLOWED_TOPICS:
                self._send_json(400, {
                    "status": "ERROR",
                    "message": f"Invalid topic '{topic}'. Must be one of: {sorted(ALLOWED_TOPICS)}"
                })
                return

            if voice not in ALLOWED_VOICES:
                self._send_json(400, {
                    "status": "ERROR",
                    "message": f"Invalid voice '{voice}'. Must be one of: {sorted(ALLOWED_VOICES)}"
                })
                return

            # Enqueue asynchronous job
            job_id = uuid.uuid4().hex
            with JOBS_LOCK:
                JOBS[job_id] = {
                    "job_id": job_id,
                    "topic": topic,
                    "voice": voice,
                    "status": "queued",
                    "created_at": os.path.getmtime(OUTPUT_DIR) if os.path.exists(OUTPUT_DIR) else 0
                }

            thread = threading.Thread(target=async_render_worker, args=(job_id, topic, voice), daemon=True)
            thread.start()

            self._send_json(202, {
                "status": "QUEUED",
                "job_id": job_id,
                "status_url": f"/api/job-status?job_id={job_id}"
            })
            return

        elif path == "/api/upload":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8")) if body else {}
            except json.JSONDecodeError:
                self._send_json(400, {"status": "ERROR", "message": "Malformed JSON payload."})
                return

            video_file = data.get("video_file")
            privacy = data.get("privacy", "private")

            if not video_file:
                self._send_json(400, {"status": "ERROR", "message": "Missing 'video_file' in payload."})
                return

            if privacy not in ALLOWED_PRIVACY:
                self._send_json(400, {"status": "ERROR", "message": f"Invalid privacy status '{privacy}'."})
                return

            safe_video_path = os.path.join(OUTPUT_DIR, os.path.basename(video_file))
            if not os.path.exists(safe_video_path):
                self._send_json(404, {"status": "ERROR", "message": "Specified video file not found."})
                return

            publisher = YouTubePublisher()
            try:
                upload_result = publisher.upload_video(
                    video_path=safe_video_path,
                    title="AI Tech Mystery #Shorts",
                    description="Educational tech mystery.",
                    tags=["Tech", "Shorts"],
                    privacy_status=privacy
                )
                self._send_json(200, upload_result)
            except Exception as e:
                logger.error(f"Upload execution error: {str(e)}", exc_info=True)
                self._send_json(500, {"status": "ERROR", "message": "Upload request failed. Check server logs."})
            return

        else:
            self.send_response(404)
            self.end_headers()

def start_server(port: int = 8080):
    server = HTTPServer(("127.0.0.1", port), StudioHandler)
    logger.info(f"Vortex Shorts Studio Web Server running at: http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down.")
        server.server_close()

if __name__ == "__main__":
    start_server(8080)
