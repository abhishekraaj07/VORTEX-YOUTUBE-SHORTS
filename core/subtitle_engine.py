"""
Subtitle Engine: Advanced SubStation Alpha (.ass) Generator for YouTube Shorts
Renders Hormozi/MrBeast style bold animated glowing subtitles with YouTube UI Safe Margins.
"""

import os
from typing import List
from .voice_engine import WordTiming

class SubtitleEngine:
    """Generates broadcast-grade vertical subtitles (.ass format) for 1080x1920 Shorts."""

    ASS_HEADER = """[Script Info]
Title: Viral YouTube Shorts Captions
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,68,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,6,3,2,60,60,480,1
Style: Highlight,Arial,74,&H0000F5FF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,105,105,2,0,1,8,4,2,60,60,480,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    @staticmethod
    def _format_time(ms: int) -> str:
        """Converts milliseconds to ASS timestamp H:MM:SS.cs"""
        hours = ms // 3600000
        ms %= 3600000
        minutes = ms // 60000
        ms %= 60000
        seconds = ms // 1000
        centiseconds = (ms % 1000) // 10
        return f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

    def generate_ass(
        self,
        word_timings: List[WordTiming],
        output_ass_path: str,
        chunk_size: int = 3
    ) -> str:
        """
        Groups words into fast 2-3 word energetic chunks with active word highlighting.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_ass_path)), exist_ok=True)
        
        events = []
        n = len(word_timings)
        i = 0

        while i < n:
            chunk = word_timings[i : min(i + chunk_size, n)]
            if not chunk:
                break
            
            chunk_start = chunk[0].start_ms
            chunk_end = chunk[-1].end_ms
            
            # Make sure minimum display time is at least 350ms
            if chunk_end - chunk_start < 350:
                chunk_end = chunk_start + 350

            # Sub-events for each word in chunk being highlighted
            for w_idx, active_word in enumerate(chunk):
                w_start = max(chunk_start, active_word.start_ms)
                w_end = min(chunk_end, active_word.end_ms)
                if w_end <= w_start:
                    w_end = w_start + 250

                line_parts = []
                for other_w in chunk:
                    clean_w = other_w.word.strip().upper()
                    if other_w == active_word:
                        # Glowing Yellow / Cyan active word
                        line_parts.append(r"{\c&H00D7FF&\3c&H000000&\b1}" + clean_w + r"{\r}")
                    else:
                        line_parts.append(r"{\c&H00FFFFFF&\3c&H000000&\b1}" + clean_w + r"{\r}")

                line_text = " ".join(line_parts)
                start_str = self._format_time(w_start)
                end_str = self._format_time(w_end)
                events.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{line_text}")

            i += chunk_size

        with open(output_ass_path, "w", encoding="utf-8") as f:
            f.write(self.ASS_HEADER)
            f.write("\n".join(events))
            f.write("\n")

        return output_ass_path
