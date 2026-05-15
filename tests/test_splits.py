import os
import json
import pytest
import numpy as np
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from step_1_generate_splits import generate_splits

def test_generate_splits(tmp_path):
    # Create a config
    config_file = tmp_path / "config.yaml"
    output_dir = tmp_path / "outputs"
    config_file.write_text(f"dataset: spiral\nmodel: mlp\nseed: 42\noutput_dir: {output_dir}")
    
    # Run split generation
    generate_splits(str(config_file))
    
    # Check artifacts
    assert (output_dir / "retain_indices.npy").exists()
    assert (output_dir / "forget_indices.npy").exists()
    assert (output_dir / "validation_indices.npy").exists()
    assert (output_dir / "test_indices.npy").exists()
    assert (output_dir / "split_metadata.json").exists()
    assert (output_dir / "validation_report.json").exists()
    assert (output_dir / "status.json").exists()
    
    # Load indices and check for overlaps
    retain = np.load(output_dir / "retain_indices.npy")
    forget = np.load(output_dir / "forget_indices.npy")
    val = np.load(output_dir / "validation_indices.npy")
    test = np.load(output_dir / "test_indices.npy")
    
    retain_set = set(retain)
    forget_set = set(forget)
    val_set = set(val)
    test_set = set(test)
    
    assert len(retain_set.intersection(forget_set)) == 0
    assert len(retain_set.intersection(val_set)) == 0
    assert len(forget_set.intersection(val_set)) == 0
    assert len(retain_set.intersection(test_set)) == 0
    
    # Check if we run without overwrite it doesn't fail but skips
    # Actually just test it runs without error
    generate_splits(str(config_file))
    
    # Test metadata
    with open(output_dir / "split_metadata.json", "r") as f:
        meta = json.load(f)
        assert meta["total_size"] == 1000
        assert meta["retain_size"] + meta["forget_size"] + meta["validation_size"] + meta["test_size"] == 1000
