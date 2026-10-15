# ⚡ Vortex YouTube Shorts Engine — Autonomous Monetized Production

A high-performance, autonomous YouTube Shorts and video production pipeline engineered for **80%+ audience retention**, **word-level animated kinetic typography**, **hyper-realistic neural voices**, and **strict YouTube 2026 AI & Synthetic Media policy compliance**.

---

## 🎯 Monetization & Compliance Architecture (YouTube 2026)

YouTube rejects low-effort, repetitive, or generic AI slideshows. This engine enforces monetization eligibility through:
1. **Curiosity Hook + Retention Flow:** 0–3s high-retention hook, informative pacing, and an infinite-loop ending.
2. **Natural Human Neural Voices:** Microsoft Neural Voices (`hi-IN-MadhurNeural`, `hi-IN-SwaraNeural`, `en-IN-PrabhatNeural`, `en-US-ChristopherNeural`) with custom tempo (+6%).
3. **Burned-In Kinetic ASS Typography:** Vertical 1080x1920 styled captions with active word highlighting, high-contrast borders, and YouTube UI safety zone padding.
4. **Synthetic Media Declaration:** Uploads include `containsSyntheticMedia: true` to avoid shadowbans and maintain trust.

---

## 🚀 Quick Start

### 1. Render a Short via Terminal
```powershell
cd c:\antigravity_os_automation\youtube_engine

# Render default viral tech mystery (Year 2038 Bug) in Hindi
python run_pipeline.py --topic y2k38_bug --output y2k38_viral_short.mp4

# Render Undersea Cables short in English
python run_pipeline.py --topic undersea_cables --voice en_male --output cables_short.mp4
```

### 2. Launch Cyber Web Studio (Interactive Dashboard)
```powershell
python server.py
```
Open **[http://localhost:8080](http://localhost:8080)** in your browser to:
- Select trending niches and topics.
- Preview rendered 1080x1920 videos directly inside an interactive mobile player.
- Copy title, description, and tags with 1-click.
- Download MP4 or publish to YouTube.

---

## 📡 Automatic YouTube Uploading (Optional Setup)
To publish directly to your channel:
1. Go to [Google Cloud Console](https://console.cloud.google.com/) and enable the **YouTube Data API v3**.
2. Download OAuth 2.0 Client Credentials as `client_secrets.json` and place it in `youtube_engine/`.
3. Run `python run_pipeline.py --upload` to authenticate once and automate publishing.
