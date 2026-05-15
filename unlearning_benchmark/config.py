import yaml
import copy

def load_config(path: str) -> dict:
    """Loads a YAML configuration file."""
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config if config is not None else {}

def validate_config(config: dict) -> None:
    """Validates that required keys are present in the config."""
    required_keys = ['dataset', 'model', 'seed']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")

def save_config(config: dict, path: str) -> None:
    """Saves a configuration dictionary to a YAML file."""
    with open(path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def update_config(base_config: dict, overrides: dict) -> dict:
    """Updates a configuration with overrides (shallow update)."""
    new_config = copy.deepcopy(base_config)
    new_config.update(overrides)
    return new_config
