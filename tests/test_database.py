import os
import pytest
from core.database import Database

def test_database_init_and_tables(tmp_path):
    db_file = str(tmp_path / "test_vortex.db")
    db = Database(db_path=db_file)
    assert os.path.exists(db_file)
    
    # Check tables created
    with db._get_connection() as conn:
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    assert "jobs" in tables
    assert "videos" in tables
    assert "uploads" in tables

def test_job_crud_lifecycle(tmp_path):
    db_file = str(tmp_path / "test_vortex.db")
    db = Database(db_path=db_file)
    
    # Create
    job = db.create_job("job_123", "y2k38_bug", "hi_male")
    assert job["id"] == "job_123"
    assert job["status"] == "queued"
    
    # Update
    db.update_job_status("job_123", "rendering", progress=50)
    job_updated = db.get_job("job_123")
    assert job_updated["status"] == "rendering"
    assert job_updated["progress"] == 50
    
    # Complete
    db.update_job_status("job_123", "completed", progress=100)
    job_done = db.get_job("job_123")
    assert job_done["status"] == "completed"

def test_video_save_and_retrieval(tmp_path):
    db_file = str(tmp_path / "test_vortex.db")
    db = Database(db_path=db_file)
    
    db.save_video(
        video_id="vid_001",
        job_id=None,
        topic="stuxnet_virus",
        title="Stuxnet Cyber Weapon",
        duration=58.5,
        size_mb=35.2,
        video_path="output/stuxnet.mp4",
        metadata={"tags": ["Stuxnet", "Cyber"]}
    )
    
    video = db.get_video("vid_001")
    assert video is not None
    assert video["title"] == "Stuxnet Cyber Weapon"
    assert video["duration"] == 58.5
    assert video["metadata"]["tags"] == ["Stuxnet", "Cyber"]
    
    videos_list = db.list_videos()
    assert len(videos_list) == 1
