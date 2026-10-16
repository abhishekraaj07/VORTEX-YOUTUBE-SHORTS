import pytest
from core.script_generator import ScriptGenerator, VideoScript, VIRAL_TEMPLATES

def test_template_retrieval_valid():
    script = ScriptGenerator.get_template("y2k38_bug")
    assert isinstance(script, VideoScript)
    assert script.topic_id == "y2k38_bug"
    assert "2038" in script.title
    assert len(script.story_chunks) > 0
    assert script.estimated_duration_sec > 20
    assert script.category_id == "28"

def test_template_retrieval_fallback():
    script = ScriptGenerator.get_template("non_existent_topic")
    assert script.topic_id == "y2k38_bug"

def test_custom_script_generation():
    script = ScriptGenerator.create_custom_script(
        topic="Quantum Computing Paradox",
        hook="Can a computer be in two places at once?",
        points=["Point 1 explanation.", "Point 2 explanation."],
        loop_phrase="And that is quantum reality."
    )
    assert script.topic_id == "custom"
    assert "Quantum Computing" in script.title
    assert len(script.story_chunks) == 2
    assert script.full_narration.startswith("Can a computer")

def test_list_templates():
    templates = ScriptGenerator.list_available_templates()
    assert len(templates) == len(VIRAL_TEMPLATES)
    assert any(t["id"] == "stuxnet_virus" for t in templates)
