import os
import pytest
from unlearning_benchmark.config import load_config, validate_config, save_config, update_config

def test_load_config(tmp_path):
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text("dataset: spiral\nmodel: mlp\nseed: 42")
    
    config = load_config(str(config_file))
    assert config['dataset'] == 'spiral'
    assert config['model'] == 'mlp'
    assert config['seed'] == 42

def test_validate_config_success():
    config = {'dataset': 'spiral', 'model': 'mlp', 'seed': 42}
    validate_config(config)

def test_validate_config_missing_key():
    config = {'dataset': 'spiral', 'model': 'mlp'}
    with pytest.raises(ValueError, match="Missing required configuration key: seed"):
        validate_config(config)

def test_save_config(tmp_path):
    config = {'dataset': 'spiral', 'model': 'mlp', 'seed': 42}
    config_file = tmp_path / "saved_config.yaml"
    
    save_config(config, str(config_file))
    
    loaded_config = load_config(str(config_file))
    assert loaded_config == config

def test_update_config():
    base_config = {'dataset': 'spiral', 'model': 'mlp', 'seed': 42, 'unlearning': {'epochs': 10}}
    overrides = {'seed': 100, 'model': 'resnet18'}
    
    new_config = update_config(base_config, overrides)
    
    assert new_config['seed'] == 100
    assert new_config['model'] == 'resnet18'
    assert new_config['dataset'] == 'spiral'
    assert base_config['seed'] == 42
