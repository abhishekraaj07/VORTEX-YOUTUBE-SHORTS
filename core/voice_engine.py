"""
Voice Engine: High-Definition Speech Synthesis with Sentence & Word Timing
Powered by edge-tts (Microsoft Neural Speech API)
"""

import os
import asyncio
import json
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional
import edge_tts

@dataclass
class WordTiming:
    word: str
    start_ms: int
    end_ms: int
    duration_ms: int

class VoiceEngine:
    """Generates natural human-like voiceovers with word-level synchronization."""

    VOICE_MAP = {
        "hi_male": "hi-IN-MadhurNeural",
        "hi_female": "hi-IN-SwaraNeural",
        "en_male": "en-IN-PrabhatNeural",
        "en_female": "en-IN-NeerjaExpressiveNeural",
        "en_us_male": "en-US-ChristopherNeural"
    }

    def __init__(self, voice_key: str = "hi_male", rate: str = "+6%", pitch: str = "+0Hz"):
        self.voice = self.VOICE_MAP.get(voice_key, "hi-IN-MadhurNeural")
        self.rate = rate
        self.pitch = pitch

    async def generate_speech_async(
        self,
        text: str,
        output_audio_path: str,
        output_timing_path: Optional[str] = None
    ) -> Tuple[str, List[WordTiming]]:
        """Synthesizes speech and extracts sentence boundaries and interpolated word timings."""
        os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)
        
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            pitch=self.pitch
        )
        
        word_timings: List[WordTiming] = []
        sentence_boundaries = []

        with open(output_audio_path, "wb") as audio_file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] in ("SentenceBoundary", "WordBoundary"):
                    offset_ms = int(chunk["offset"] / 10000)
                    duration_ms = int(chunk["duration"] / 10000)
                    chunk_text = chunk["text"].strip()
                    
                    if chunk["type"] == "WordBoundary":
                        word_timings.append(WordTiming(
                            word=chunk_text,
                            start_ms=offset_ms,
                            end_ms=offset_ms + duration_ms,
                            duration_ms=duration_ms
                        ))
                    else:
                        sentence_boundaries.append((offset_ms, duration_ms, chunk_text))

        # If edge_tts returned SentenceBoundary events, interpolate words within each sentence
        if not word_timings and sentence_boundaries:
            for s_start, s_dur, s_text in sentence_boundaries:
                words = s_text.split()
                if not words:
                    continue
                total_chars = sum(len(w) for w in words)
                if total_chars == 0:
                    continue
                
                curr_start = s_start
                for w in words:
                    # Allocate time based on character length ratio
                    w_dur = max(180, int((len(w) / total_chars) * s_dur))
                    word_timings.append(WordTiming(
                        word=w,
                        start_ms=curr_start,
                        end_ms=curr_start + w_dur,
                        duration_ms=w_dur
                    ))
                    curr_start += w_dur

        if output_timing_path:
            with open(output_timing_path, "w", encoding="utf-8") as tf:
                json.dump([wt.__dict__ for wt in word_timings], tf, indent=2, ensure_ascii=False)

        return output_audio_path, word_timings

    def generate_speech(
        self,
        text: str,
        output_audio_path: str,
        output_timing_path: Optional[str] = None
    ) -> Tuple[str, List[WordTiming]]:
        return asyncio.run(self.generate_speech_async(text, output_audio_path, output_timing_path))
