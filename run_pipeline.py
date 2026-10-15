"""
Autonomous YouTube Video Production Pipeline
Executes End-to-End Generation: Script -> Voiceover -> ASS Subtitles -> Visuals -> FFmpeg Assembly -> Upload Check
"""

import os
import sys
import argparse
import json
import time

# Ensure package is resolvable and utf-8 encoding for Windows console
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from core.script_generator import ScriptGenerator
from core.voice_engine import VoiceEngine
from core.subtitle_engine import SubtitleEngine
from core.visual_generator import VisualGenerator
from core.composer import VideoComposer
from core.uploader import YouTubePublisher

def run_pipeline(
    topic_id: str = "y2k38_bug",
    voice_key: str = "hi_male",
    output_filename: str = "viral_short.mp4",
    auto_upload: bool = False
):
    print("=" * 65)
    print("  🎬 AUTONOMOUS YOUTUBE SHORTS ENGINE — FULL PRODUCTION PIPELINE")
    print("=" * 65)
    
    start_time = time.time()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Script Generation
    print("\n[Step 1/5] 📝 Generating Retention-Engineered Viral Script...")
    script = ScriptGenerator.get_template(topic_id)
    print(f"  • Niche: {script.niche}")
    print(f"  • Title: {script.title}")
    print(f"  • Words: {len(script.full_narration.split())} words (~{script.estimated_duration_sec}s)")
    
    script_meta_path = os.path.join(output_dir, f"{topic_id}_metadata.json")
    with open(script_meta_path, "w", encoding="utf-8") as f:
        json.dump(script.__dict__, f, indent=2, ensure_ascii=False)
        
    # 2. Voice Synthesis & Word Timings
    print("\n[Step 2/5] 🎙️ Synthesizing Neural Voiceover & Extracting Word Timings...")
    audio_path = os.path.join(output_dir, f"{topic_id}_voice.mp3")
    timing_path = os.path.join(output_dir, f"{topic_id}_timings.json")
    
    voice_engine = VoiceEngine(voice_key=voice_key, rate="+6%")
    audio_path, word_timings = voice_engine.generate_speech(
        text=script.full_narration,
        output_audio_path=audio_path,
        output_timing_path=timing_path
    )
    print(f"  • Voiceover saved: {audio_path}")
    print(f"  • Captured: {len(word_timings)} precise word timing boundaries.")

    # 3. Subtitle Generation (.ass)
    print("\n[Step 3/5] 💬 Rendering High-Converting Kinetic Subtitles (ASS)...")
    ass_path = os.path.join(output_dir, f"{topic_id}_captions.ass")
    sub_engine = SubtitleEngine()
    sub_engine.generate_ass(
        word_timings=word_timings,
        output_ass_path=ass_path,
        chunk_size=3
    )
    print(f"  • Burned-in ASS Subtitles ready: {ass_path}")

    # 4. Visual Motion Background (Thematic Scene Images + Ken Burns Zoom)
    print("\n[Step 4/5] 🌌 Synthesizing Thematic Multi-Scene Background Video...")
    duration = VideoComposer.get_audio_duration(audio_path)
    bg_video_path = os.path.join(output_dir, f"{topic_id}_bg.mp4")
    
    images_dir = os.path.join(base_dir, "assets", "images", topic_id)
    scene_images = []
    if os.path.exists(images_dir):
        scene_images = [
            os.path.join(images_dir, f) for f in sorted(os.listdir(images_dir))
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
        print(f"  • Found {len(scene_images)} cinematic scene images for '{topic_id}'")

    if scene_images:
        VisualGenerator.generate_scene_video(
            image_paths=scene_images,
            total_duration_sec=duration + 0.5,
            output_path=bg_video_path,
            fps=30
        )
    else:
        VisualGenerator.generate_cyber_background(
            duration_sec=duration + 0.5,
            output_path=bg_video_path,
            fps=30
        )
    print(f"  • Dynamic Scene Video generated ({duration:.1f}s): {bg_video_path}")

    # 5. FFmpeg Video Assembly
    print("\n[Step 5/5] ⚡ Composing Final 1080x1920 60FPS Video with Burned Subtitles...")
    final_video_path = os.path.join(output_dir, output_filename)
    VideoComposer.compose_video(
        background_video_path=bg_video_path,
        voiceover_audio_path=audio_path,
        subtitle_ass_path=ass_path,
        output_mp4_path=final_video_path
    )
    
    file_size_mb = os.path.getsize(final_video_path) / (1024 * 1024)
    elapsed = time.time() - start_time
    print(f"\n🎉 SUCCESS! Video Ready in {elapsed:.1f} seconds!")
    print(f"  • Path: {final_video_path}")
    print(f"  • Resolution: 1080x1920 (Vertical 9:16)")
    print(f"  • Size: {file_size_mb:.2f} MB")
    print(f"  • Duration: {duration:.1f}s")
    
    # 6. Upload Assessment
    publisher = YouTubePublisher()
    upload_res = publisher.upload_video(
        video_path=final_video_path,
        title=script.title,
        description=script.description,
        tags=script.tags
    )
    print(f"\n📡 YouTube Publishing Status: {upload_res['status']}")
    print(f"  • Details: {upload_res.get('message', 'Ready')}")

    return {
        "video_path": final_video_path,
        "metadata_path": script_meta_path,
        "duration": duration,
        "size_mb": file_size_mb,
        "upload_status": upload_res
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous YouTube Shorts Generator")
    parser.add_argument("--topic", default="y2k38_bug", choices=["y2k38_bug", "undersea_cables", "stuxnet_virus"])
    parser.add_argument("--voice", default="hi_male", choices=["hi_male", "hi_female", "en_male", "en_female", "en_us_male"])
    parser.add_argument("--output", default="y2k38_viral_short.mp4")
    parser.add_argument("--upload", action="store_true")
    
    args = parser.parse_args()
    run_pipeline(
        topic_id=args.topic,
        voice_key=args.voice,
        output_filename=args.output,
        auto_upload=args.upload
    )
