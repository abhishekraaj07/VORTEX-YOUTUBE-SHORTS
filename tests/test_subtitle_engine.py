import os
import pytest
from core.voice_engine import WordTiming
from core.subtitle_engine import SubtitleEngine

def test_ass_time_formatting():
    engine = SubtitleEngine()
    # 0 ms -> 0:00:00.00
    assert engine._format_time(0) == "0:00:00.00"
    # 1500 ms -> 0:00:01.50
    assert engine._format_time(1500) == "0:00:01.50"
    # 65000 ms -> 0:01:05.00
    assert engine._format_time(65000) == "0:01:05.00"

def test_generate_ass_file(tmp_path):
    engine = SubtitleEngine()
    timings = [
        WordTiming(word="Duniya", start_ms=100, end_ms=500, duration_ms=400),
        WordTiming(word="bhar", start_ms=500, end_ms=900, duration_ms=400),
        WordTiming(word="ke", start_ms=900, end_ms=1200, duration_ms=300),
        WordTiming(word="servers", start_ms=1200, end_ms=1700, duration_ms=500),
    ]
    out_file = str(tmp_path / "test.ass")
    engine.generate_ass(timings, out_file, chunk_size=2)
    
    assert os.path.exists(out_file)
    with open(out_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "[Script Info]" in content
    assert "PlayResX: 1080" in content
    assert "PlayResY: 1920" in content
    assert "Dialogue:" in content
    assert "DUNIYA" in content
