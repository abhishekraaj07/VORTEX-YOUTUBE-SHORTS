"""
Visual Generator: Dynamic Multi-Scene Video Backgrounds with Ken Burns Motion
Generates high-retention vertical 1080x1920 footage from thematic scene imagery.
"""

import os
import subprocess
from typing import List, Optional

class VisualGenerator:
    """Generates 1080x1920 vertical video backgrounds with multi-scene image transitions."""

    @staticmethod
    def generate_scene_video(
        image_paths: List[str],
        total_duration_sec: float,
        output_path: str,
        fps: int = 30
    ) -> str:
        """
        Takes multiple scene images and creates a dynamic video with smooth Ken Burns zoom.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        temp_dir = os.path.join(os.path.dirname(output_path), "temp_scenes")
        os.makedirs(temp_dir, exist_ok=True)

        if not image_paths:
            return VisualGenerator.generate_cyber_background(total_duration_sec, output_path, fps)

        num_scenes = len(image_paths)
        dur_per_scene = total_duration_sec / num_scenes
        frames_per_scene = int(dur_per_scene * fps)

        scene_clips = []
        for idx, img in enumerate(image_paths):
            clip_path = os.path.join(temp_dir, f"clip_{idx}.mp4")
            
            # Ken Burns zoompan filter (slow zoom-in)
            filter_str = (
                f"scale=1080:1920:force_original_aspect_ratio=increase,"
                f"crop=1080:1920,"
                f"zoompan=z='min(zoom+0.0008,1.15)':d={frames_per_scene}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps},"
                f"vignette=PI/4:aspect=9/16,"
                f"format=yuv420p"
            )

            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", img,
                "-t", f"{dur_per_scene:.2f}",
                "-vf", filter_str,
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                clip_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0 and os.path.exists(clip_path):
                scene_clips.append(clip_path)

        if not scene_clips:
            return VisualGenerator.generate_cyber_background(total_duration_sec, output_path, fps)

        # Concatenate all clips
        concat_txt = os.path.join(temp_dir, "concat.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for c in scene_clips:
                clean_c = c.replace("\\", "/")
                f.write(f"file '{clean_c}'\n")

        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            "-t", str(total_duration_sec),
            "-c", "copy",
            output_path
        ]
        subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return output_path

    @staticmethod
    def generate_cyber_background(
        duration_sec: float,
        output_path: str,
        fps: int = 30
    ) -> str:
        """Fallback procedural cyber background."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        filter_complex = (
            f"color=c=0x070b14:s=1080x1920:d={duration_sec}:r={fps},"
            f"drawgrid=width=120:height=120:thickness=1:color=0x1e293b@0.45,"
            f"vignette=PI/3.2:aspect=9/16,"
            f"format=yuv420p"
        )
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", filter_complex,
            "-t", str(duration_sec),
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path
