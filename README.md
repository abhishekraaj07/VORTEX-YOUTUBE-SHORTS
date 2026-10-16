# ⚡ VORTEX YouTube Shorts Engine — Autonomous Production Studio & Astro Spatial OS

[![CI Test Suite](https://github.com/abhishekraaj07/VORTEX-YOUTUBE-SHORTS/actions/workflows/ci.yml/badge.svg)](https://github.com/abhishekraaj07/VORTEX-YOUTUBE-SHORTS/actions/workflows/ci.yml)
[![Tests Passing](https://img.shields.io/badge/tests-15%20passed-emerald)](https://github.com/abhishekraaj07/VORTEX-YOUTUBE-SHORTS)
[![Python Version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Astro Version](https://img.shields.io/badge/astro-4.16-orange)](https://astro.build/)
[![SQLite Database](https://img.shields.io/badge/database-SQLite%20WAL-sky)](https://www.sqlite.org/)
[![YouTube AI Policy](https://img.shields.io/badge/YouTube%202026-AI%20Policy%20Compliant-red)](https://support.google.com/youtube/answer/14328491)
[![Cloudflare Deployed](https://img.shields.io/badge/Cloudflare-Live%20Studio-amber)](https://youtube-engine.abhishekraaj07.workers.dev)

A modular, production-engineered autonomous engine for generating high-retention vertical (1080x1920) YouTube Shorts with **multi-scene Ken Burns imagery**, **Microsoft Neural Voiceover**, **broadcast kinetic typography (.ass)**, **SQLite WAL persistence**, and a **VisionOS-style Liquid Glass Spatial UI** built in **Astro.js**.

---

## 🌐 Live Deployments

* ⚡ **Cloudflare Production Studio:** [https://youtube-engine.abhishekraaj07.workers.dev](https://youtube-engine.abhishekraaj07.workers.dev)
* 🐙 **GitHub Pages Studio:** [https://abhishekraaj07.github.io/VORTEX-YOUTUBE-SHORTS/](https://abhishekraaj07.github.io/VORTEX-YOUTUBE-SHORTS/)

---

## ✨ Key Features & Architecture

### 1. 🎛️ Astro.js Liquid Glass Spatial OS (`astro-studio/`)
* **VisionOS Aesthetic**: Multi-layered frosted glassmorphism (`backdrop-filter: blur(28px)`), specular light sheen, dynamic chromatic liquid light orbs, and interactive 3D parallax card tilt.
* **Pure Web Audio Synthesizer**: Zero external audio assets; synthesizes real-time high-frequency glass crystal chimes and haptic feedback on user interactions.
* **Modular Multi-View Navigation Dock**:
  * **🎛️ Studio Core**: Concept selector, script breakdown, neural voice tuner, and one-click render trigger.
  * **⚡ Neural Pipeline**: Real-time 6-stage node flowchart, stage latency tracking, and live terminal logger.
  * **🎞️ Media Vault**: Database-driven catalog of all generated shorts with 9:16 VisionOS theater playback and 1-click MP4 downloads.
  * **🛡️ YouTube Compliance**: Interactive 2026 AI policy verification checklist and protected upload station.
  * **⚙️ Spatial Matrix**: Local/remote backend switcher, SQLite WAL telemetry, and sound synthesizer controls.

### 2. 🗄️ Relational Database Engine (`core/database.py`)
* **SQLite 3 in WAL Mode (Write-Ahead Logging)**: High-concurrency, zero-lock architecture for simultaneous rendering workers and HTTP queries.
* **Relational Schema**:
  * `jobs`: Tracks UUID job lifecycle (`queued` ➔ `rendering` ➔ `completed` / `failed`), progress percentage, and error logging.
  * `videos`: Permanent catalog storing video path, duration, file size, topic, title, and full metadata JSON.
  * `uploads`: YouTube publishing audit trail with YouTube video IDs and privacy status.

### 3. 🛡️ YouTube 2026 AI Policy Compliance Guardrails
* **Automated Synthetic Media Disclosure**: Injects the official YouTube Generative AI disclosure notice directly into every video description:
  > *"ℹ️ AI / Synthetic Content Disclosure: Sound, narration, or visuals in this video were digitally generated or meaningfully altered using AI tools in compliance with YouTube Community Guidelines."*
* **Anti-Slop / Originality Architecture**: Uses multi-scene dynamic Ken Burns visual compositions and transformative educational narratives to avoid reused/repetitive content penalties.
* **Strict Privacy Gate**: All uploads default strictly to `private` status. No video goes public without explicit human-in-the-loop creator confirmation.
* **Metadata Validation**: Strict validation enforcing titles $\le 100$ characters, sanitized tags, and default category assignment (Science & Technology - ID 28).

### 4. ⚡ High-Speed Rendering Pipeline
* **Script Engine (`core/script_generator.py`)**: 0–3 second curiosity hook, concise educational story points, and seamless loop closures.
* **Neural Voice (`core/voice_engine.py`)**: Microsoft Neural TTS (`hi-IN-MadhurNeural`, `en-IN-PrabhatNeural`, etc.) with sentence boundary capture and character-proportional word timing interpolation.
* **Kinetic Captions (`core/subtitle_engine.py`)**: SubStation Alpha (`.ass`) typography with glowing highlights (`&H00D7FF&` Cyber Yellow) positioned strictly within the YouTube UI vertical safety zone.
* **Dynamic Compositor (`core/composer.py`)**: Fast multi-scene image assembly with slow Ken Burns motion, cinematic vignette, and 1080x1920 30fps H.264 MP4 rendering.

---

## 🚀 Quick Start

### 1. Prerequisites
* **Python 3.12+**
* **Node.js 20+** & **npm**
* **FFmpeg** installed and added to your system `PATH`

### 2. Clone and Setup
```bash
git clone https://github.com/abhishekraaj07/VORTEX-YOUTUBE-SHORTS.git
cd VORTEX-YOUTUBE-SHORTS

# Install Python dependencies
pip install -r requirements.txt

# Install Astro Studio dependencies
cd astro-studio
npm install
cd ..
```

### 3. Run Pipeline via Terminal (CLI Mode)
```bash
# Generate viral tech mystery (Year 2038 Bug)
python run_pipeline.py --topic y2k38_bug --output y2k38_viral_short.mp4

# Generate with English voice and private upload
python run_pipeline.py --topic undersea_cables --voice en_male --output cables_short.mp4 --upload --privacy private
```

### 4. Launch Local Web Studio (Python Server + Astro)
```bash
python server.py
```
Open **[http://localhost:8080](http://localhost:8080)** in your browser.

### 5. Develop in Astro Studio (Hot-Reload Mode)
```bash
cd astro-studio
npm run dev
```
Open **[http://localhost:4321](http://localhost:4321)**. When ready, build production static assets directly to `../web`:
```bash
npm run build
```

### 6. Run Automated Test Suite (15 Unit Tests)
```bash
pytest
```
All 15 tests will execute and pass:
```text
tests\test_database.py ....                                              [ 26%]
tests\test_script_generator.py ....                                      [ 53%]
tests\test_security_validation.py .....                                  [ 86%]
tests\test_subtitle_engine.py ..                                         [100%]
============================= 15 passed in 1.42s ==============================
```

---

## 📡 REST API Reference

The backend provides hardened, non-blocking REST endpoints:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the Astro Liquid Glass Spatial UI studio. |
| `POST` | `/api/render` | Enqueues an asynchronous render job in SQLite (`202 Accepted`). |
| `GET` | `/api/job-status?job_id=...` | Reads live job status, progress percentage, and video URL. |
| `GET` | `/api/history` | Fetches the video catalog and recent job history from SQLite. |
| `GET` | `/api/templates` | Returns all viral script templates, retention hooks, and metadata. |
| `GET` | `/api/system-stats` | Returns real-time database stats, worker threads, and system telemetry. |
| `GET` | `/video?file=...` | Delivers 64KB chunked video streaming with full HTTP Range seek support. |
| `POST` | `/api/upload` | Validates metadata and executes YouTube Data API v3 upload. |

---

## 📁 Repository Structure

```
VORTEX-YOUTUBE-SHORTS/
├── .github/workflows/
│   ├── ci.yml                 # Automated pytest CI pipeline on Python 3.12
│   └── deploy-pages.yml       # GitHub Pages deployment workflow
├── assets/                    # Scene assets and reference images
├── astro-studio/              # Modular Astro.js 4.16 Frontend Project
│   ├── astro.config.mjs       # Astro config (Tailwind + output to ../web)
│   ├── package.json           # Astro dependencies
│   ├── tailwind.config.mjs    # Tailwind styling configuration
│   └── src/
│       ├── layouts/Layout.astro
│       ├── styles/global.css
│       ├── pages/index.astro
│       └── components/
│           ├── Header.astro
│           ├── StudioCore.astro
│           ├── PhoneStage.astro
│           ├── PipelineGraph.astro
│           ├── MediaVault.astro
│           ├── YouTubeCompliance.astro
│           ├── SystemMatrix.astro
│           └── TheaterModal.astro
├── core/
│   ├── composer.py            # FFmpeg multi-scene video assembler
│   ├── database.py            # SQLite WAL relational storage engine
│   ├── script_generator.py    # Retention-engineered script engine
│   ├── subtitle_engine.py     # SubStation Alpha (.ass) generator
│   ├── uploader.py            # YouTube Data API v3 publisher & policy validator
│   ├── visual_generator.py    # Ken Burns zoom & motion compositor
│   └── voice_engine.py        # Neural speech synthesis with word timings
├── output/                    # Rendered 1080x1920 MP4 outputs & metadata
├── tests/                     # 15 automated unit tests
│   ├── test_database.py
│   ├── test_script_generator.py
│   ├── test_security_validation.py
│   └── test_subtitle_engine.py
├── web/                       # Compiled production web bundle served by Cloudflare
│   ├── _astro/                # Optimized CSS & asset chunks
│   └── index.html             # Compiled entry point
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Pinned Python dependencies
├── run_pipeline.py            # CLI pipeline orchestrator
├── server.py                  # Asynchronous HTTP server & REST API
└── wrangler.jsonc             # Cloudflare Workers / Pages configuration
```

---

## 🔒 Security & Safe Publishing

1. **Secret Hygiene**: `client_secrets.json` and `yt_token.json` are strictly excluded in `.gitignore` and never committed or exposed in client bundles.
2. **Directory Traversal Protection**: All file paths requested via `/video` and `/api/upload` are sanitized using `os.path.basename` and verified against root boundaries.
3. **Input Allowlisting**: Only verified topics, voices, and privacy modes can be submitted to `/api/render` and `/api/upload`.
4. **Creator Review Default**: All uploaded videos default to `private` mode, ensuring full creator review in YouTube Studio before public distribution.

---

## 👤 Author

Developed by **[Abhishek Raaj](https://github.com/abhishekraaj07)**.
* Repository: [abhishekraaj07/VORTEX-YOUTUBE-SHORTS](https://github.com/abhishekraaj07/VORTEX-YOUTUBE-SHORTS)
* License: MIT
