"""
Video Composer: Assembles Audio, Procedural Visuals, Ambient Sound, and Subtitles into YouTube Shorts MP4.
Powered by FFmpeg 9.0.2 with libass burned-in styling.
"""

import os
import subprocess
from typing import Optional

class VideoComposer:
    """Assembles all components into broadcast-ready 1080x1920 vertical MP4."""

    @staticmethod
    def get_audio_duration(audio_path: str) -> float:
        """Extracts exact duration in seconds using ffprobe."""
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return float(res.stdout.strip())
        return 30.0

    @classmethod
    def compose_video(
        cls,
        background_video_path: str,
        voiceover_audio_path: str,
        subtitle_ass_path: str,
        output_mp4_path: str,
        ambient_music_path: Optional[str] = None
    ) -> str:
        """
        Combines background video, voiceover audio, subtitles, and exports 1080x1920 MP4.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4_path)), exist_ok=True)
        duration = cls.get_audio_duration(voiceover_audio_path)
        
        # Format subtitle path for FFmpeg filter (escape colons and backslashes on Windows)
        escaped_ass = subtitle_ass_path.replace("\\", "/").replace(":", "\\:")
        
        video_filters = f"ass='{escaped_ass}'"

        cmd = [
            "ffmpeg", "-y",
            "-i", background_video_path,
            "-i", voiceover_audio_path
        ]

        if ambient_music_path and os.path.exists(ambient_music_path):
            cmd.extend([
                "-i", ambient_music_path,
                "-filter_complex",
                f"[0:v]{video_filters}[v];[2:a]volume=0.15[bg];[1:a][bg]amix=inputs=2:duration=first[a]",
                "-map", "[v]",
                "-map", "[a]"
            ])
        else:
            cmd.extend([
                "-filter_complex",
                f"[0:v]{video_filters}[v]",
                "-map", "[v]",
                "-map", "1:a"
            ])

        cmd.extend([
            "-t", str(duration + 0.3),
            "-c:v", "libx264",
            "-preset", "faster",
            "-crf", "19",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output_mp4_path
        ])

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg Video Composition failed: {result.stderr[:500]}")

        return output_mp4_path
