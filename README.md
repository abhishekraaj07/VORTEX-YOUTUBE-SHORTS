# ⚡ VORTEX YouTube Shorts Engine — Autonomous Production Studio

A modular, production-engineered pipeline for generating high-engagement vertical (1080x1920) YouTube Shorts with **multi-scene Ken Burns imagery**, **Microsoft Neural Voiceover**, and **word-synchronized kinetic typography (.ass)**.

---

## 🎯 Architecture & YouTube 2026 Policy Compliance

1. **Synthetic Content Disclosure:**
   In compliance with YouTube Generative AI Policies, all uploads automatically format the official YouTube synthetic disclosure notice directly in the video description:
   > *"ℹ️ AI / Synthetic Content Disclosure: Sound, narration, or visuals in this video were digitally generated or meaningfully altered using AI tools in compliance with YouTube Community Guidelines."*
2. **Safe Upload Gating:**
   Rendering is local-first. Video files remain on disk for inspection and will **never** upload to YouTube unless explicitly invoked with `--upload` (CLI) or via dedicated publish confirmation (Dashboard). Default privacy status is strictly locked to `private` for creator verification.
3. **Pacing & Retention Structure:**
   Scripts are structured with a 0–3 second curiosity hook, concise educational story points, and a seamless loop conclusion.
4. **Asynchronous Non-Blocking Server:**
   The dashboard runs an async worker thread pool with UUID job tracking, input allowlists, safe error masking, and HTTP Range-based chunked streaming.

---

## 🚀 Quick Start

### 1. Run Pipeline via Terminal (Local Generation)
```powershell
cd c:\antigravity_os_automation\youtube_engine

# Generate default viral tech mystery (Year 2038 Bug)
python run_pipeline.py --topic y2k38_bug --output y2k38_viral_short.mp4

# Generate with specific voice and private upload
python run_pipeline.py --topic undersea_cables --voice en_male --output cables_short.mp4 --upload --privacy private
```

### 2. Launch Cyber Web Studio (Interactive Dashboard)
```powershell
python server.py
```
Open **[http://localhost:8080](http://localhost:8080)** to:
- Select topics and voices with allowlist validation.
- Enqueue asynchronous rendering jobs.
- Stream and preview 1080x1920 videos inside an interactive mobile frame with seeking support.
- Download MP4 and copy validated metadata.

### 3. Run Automated Tests
```powershell
python -m pytest tests/ -v
```

---

## 📁 Repository Structure

```
youtube_engine/
├── .github/workflows/
│   └── ci.yml               # Automated GitHub Actions test pipeline
├── assets/
│   └── images/              # Thematic high-res scene images (1080x1920)
├── core/
│   ├── composer.py          # FFmpeg video, audio & subtitle assembler
│   ├── script_generator.py  # Retention-engineered script engine
│   ├── subtitle_engine.py   # Advanced SubStation Alpha (.ass) generator
│   ├── uploader.py          # YouTube Data API v3 publisher & policy validator
│   ├── visual_generator.py  # Multi-scene Ken Burns zoom & motion compositor
│   └── voice_engine.py      # Neural speech synthesis with word timings
├── output/                  # Rendered video outputs & metadata JSON
├── tests/                   # Pytest test suite (11 passing unit tests)
├── web/
│   └── index.html           # Production dark studio UI
├── requirements.txt         # Pinned dependency manifest
├── run_pipeline.py          # CLI pipeline orchestrator
└── server.py                # Asynchronous HTTP API & streaming server
```

---

## 📡 Cloud Publishing Setup (Optional)
To publish directly to your channel:
1. In the [Google Cloud Console](https://console.cloud.google.com/), enable the **YouTube Data API v3**.
2. Download your OAuth 2.0 Client Credentials as `client_secrets.json` and place it in the `youtube_engine/` directory.
3. Trigger publishing via `--upload` or the web dashboard.
