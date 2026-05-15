import os
import json
import pytest
from unlearning_benchmark.status import StatusManager

def test_status_manager(tmp_path):
    output_dir = tmp_path / "outputs"
    sm = StatusManager("test_step", str(output_dir))
    
    # Check start
    sm.start()
    status_file = output_dir / "status.json"
    assert status_file.exists()
    
    with open(status_file, "r") as f:
        data = json.load(f)
        assert data["step"] == "test_step"
        assert data["state"] == "running"
    
    # Check complete
    sm.complete()
    with open(status_file, "r") as f:
        data = json.load(f)
        assert data["state"] == "completed"
        assert "duration_seconds" in data
        
    # Check fail
    sm2 = StatusManager("test_step2", str(output_dir))
    sm2.start()
    try:
        raise ValueError("Something went wrong")
    except Exception as e:
        sm2.fail(e)
        
    with open(status_file, "r") as f:
        data = json.load(f)
        assert data["state"] == "failed"
        assert data["error_type"] == "ValueError"
        assert data["error_message"] == "Something went wrong"
