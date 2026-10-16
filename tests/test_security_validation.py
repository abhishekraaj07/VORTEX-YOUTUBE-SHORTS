import pytest
from core.uploader import YouTubePublisher
from server import ALLOWED_TOPICS, ALLOWED_VOICES, ALLOWED_PRIVACY

def test_metadata_validation_valid():
    res = YouTubePublisher.validate_metadata(
        title="Valid YouTube Title",
        description="Normal video description.",
        tags=["Tech", "Shorts", "Coding"],
        privacy_status="private"
    )
    assert res["title"] == "Valid YouTube Title"
    assert "Synthetic Content Disclosure" in res["description"]
    assert res["privacy_status"] == "private"
    assert "Tech" in res["tags"]

def test_metadata_validation_empty_title():
    with pytest.raises(ValueError, match="title cannot be empty"):
        YouTubePublisher.validate_metadata(
            title="",
            description="desc",
            tags=[],
            privacy_status="private"
        )

def test_metadata_validation_long_title():
    long_title = "A" * 101
    with pytest.raises(ValueError, match="exceeds 100 characters"):
        YouTubePublisher.validate_metadata(
            title=long_title,
            description="desc",
            tags=[],
            privacy_status="private"
        )

def test_metadata_validation_invalid_privacy():
    with pytest.raises(ValueError, match="Invalid privacy status"):
        YouTubePublisher.validate_metadata(
            title="Title",
            description="desc",
            tags=[],
            privacy_status="secret_leak"
        )

def test_server_allowlists():
    assert "y2k38_bug" in ALLOWED_TOPICS
    assert "undersea_cables" in ALLOWED_TOPICS
    assert "stuxnet_virus" in ALLOWED_TOPICS
    
    assert "hi_male" in ALLOWED_VOICES
    assert "en_male" in ALLOWED_VOICES
    
    assert "private" in ALLOWED_PRIVACY
    assert "unlisted" in ALLOWED_PRIVACY
    assert "public" in ALLOWED_PRIVACY
