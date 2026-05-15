from typing import Callable, Any, Dict

_MODELS: Dict[str, Callable] = {}
_DATASETS: Dict[str, Callable] = {}
_UNLEARNERS: Dict[str, Callable] = {}

def register_model(name: str):
    def wrapper(cls):
        _MODELS[name] = cls
        return cls
    return wrapper

def get_model(name: str) -> Callable:
    if name not in _MODELS:
        raise KeyError(f"Model '{name}' not found in registry.")
    return _MODELS[name]

def register_dataset(name: str):
    def wrapper(cls):
        _DATASETS[name] = cls
        return cls
    return wrapper

def get_dataset(name: str) -> Callable:
    if name not in _DATASETS:
        raise KeyError(f"Dataset '{name}' not found in registry.")
    return _DATASETS[name]

def register_unlearner(name: str):
    def wrapper(cls):
        _UNLEARNERS[name] = cls
        return cls
    return wrapper

def get_unlearner(name: str) -> Callable:
    if name not in _UNLEARNERS:
        raise KeyError(f"Unlearner '{name}' not found in registry.")
    return _UNLEARNERS[name]
