import pytest
import torch
import numpy as np
import unlearning_benchmark.datasets
from unlearning_benchmark.registry import get_dataset

def test_spiral_dataset():
    DatasetClass = get_dataset("spiral")
    dataset = DatasetClass(n_samples=1000, seed=42)
    
    assert len(dataset) == 1000
    
    x, y = dataset[0]
    assert isinstance(x, torch.Tensor)
    assert isinstance(y, torch.Tensor)
    assert x.shape == (2,)
    assert y.item() in {0, 1}
    
    # Test reproducibility
    dataset2 = DatasetClass(n_samples=1000, seed=42)
    assert torch.allclose(dataset.x, dataset2.x)
    assert torch.equal(dataset.y, dataset2.y)
    
    # Test different seed
    dataset3 = DatasetClass(n_samples=1000, seed=43)
    assert not torch.allclose(dataset.x, dataset3.x)
