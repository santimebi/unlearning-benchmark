import pytest
from unlearning_benchmark.registry import (
    register_model, get_model,
    register_dataset, get_dataset,
    register_unlearner, get_unlearner
)

def test_model_registry():
    @register_model("test_model")
    class TestModel:
        pass
    
    assert get_model("test_model") == TestModel
    
    with pytest.raises(KeyError, match="Model 'unknown' not found in registry."):
        get_model("unknown")

def test_dataset_registry():
    @register_dataset("test_dataset")
    class TestDataset:
        pass
    
    assert get_dataset("test_dataset") == TestDataset
    
    with pytest.raises(KeyError, match="Dataset 'unknown' not found in registry."):
        get_dataset("unknown")

def test_unlearner_registry():
    @register_unlearner("test_unlearner")
    class TestUnlearner:
        pass
    
    assert get_unlearner("test_unlearner") == TestUnlearner
    
    with pytest.raises(KeyError, match="Unlearner 'unknown' not found in registry."):
        get_unlearner("unknown")
