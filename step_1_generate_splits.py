import os
import json
import argparse
import numpy as np
from sklearn.model_selection import train_test_split

import unlearning_benchmark.datasets  # to trigger registry
from unlearning_benchmark.config import load_config
from unlearning_benchmark.registry import get_dataset
from unlearning_benchmark.status import StatusManager

def generate_splits(config_path: str, overwrite: bool = False):
    config = load_config(config_path)
    output_dir = config.get("output_dir", "./outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    status = StatusManager("step_1_generate_splits", output_dir)
    status.start()
    
    try:
        # Save config
        with open(os.path.join(output_dir, "config.yaml"), "w") as f:
            import yaml
            yaml.dump(config, f, default_flow_style=False)
            
        dataset_name = config['dataset']
        seed = config['seed']
        np.random.seed(seed)
        
        DatasetClass = get_dataset(dataset_name)
        dataset = DatasetClass(seed=seed)
        
        # Check if indices already exist
        indices_paths = {
            "retain": os.path.join(output_dir, "retain_indices.npy"),
            "forget": os.path.join(output_dir, "forget_indices.npy"),
            "validation": os.path.join(output_dir, "validation_indices.npy"),
            "test": os.path.join(output_dir, "test_indices.npy"),
        }
        
        if not overwrite and all(os.path.exists(p) for p in indices_paths.values()):
            print("Splits already exist. Use --overwrite to regenerate.")
            status.complete()
            return
        
        n_samples = len(dataset)
        all_indices = np.arange(n_samples)
        
        if dataset_name == "spiral":
            y = dataset.y.numpy()
            theta = dataset.theta
            
            # test split 20%
            train_val_idx, test_idx = train_test_split(all_indices, test_size=0.2, stratify=y, random_state=seed)
            
            # From train_val, split validation (e.g. 10% of total)
            train_idx, val_idx = train_test_split(train_val_idx, test_size=0.125, stratify=y[train_val_idx], random_state=seed)
            
            # forget set: Class 0, theta between 2*pi and 3*pi
            forget_mask = (y[train_idx] == 0) & (theta[train_idx] >= 2 * np.pi) & (theta[train_idx] <= 3 * np.pi)
            
            forget_idx = train_idx[forget_mask]
            retain_idx = train_idx[~forget_mask]
            
        else:
            raise NotImplementedError(f"Split logic for {dataset_name} not implemented yet.")
            
        # Validation checks
        retain_set = set(retain_idx)
        forget_set = set(forget_idx)
        val_set = set(val_idx)
        test_set = set(test_idx)
        
        assert len(retain_set.intersection(forget_set)) == 0, "Overlap between retain and forget"
        assert len(retain_set.intersection(val_set)) == 0, "Overlap between retain and validation"
        assert len(forget_set.intersection(val_set)) == 0, "Overlap between forget and validation"
        assert len(train_idx) + len(val_idx) + len(test_idx) == n_samples, "Split sizes don't match total"
        assert len(retain_set.intersection(test_set)) == 0, "Overlap between retain and test"
        
        # Save indices
        np.save(indices_paths["retain"], retain_idx)
        np.save(indices_paths["forget"], forget_idx)
        np.save(indices_paths["validation"], val_idx)
        np.save(indices_paths["test"], test_idx)
        
        # Metadata
        metadata = {
            "retain_size": len(retain_idx),
            "forget_size": len(forget_idx),
            "validation_size": len(val_idx),
            "test_size": len(test_idx),
            "total_size": n_samples
        }
        with open(os.path.join(output_dir, "split_metadata.json"), "w") as f:
            json.dump(metadata, f, indent=4)
            
        # Validation report
        report = {
            "retain_intersection_forget": 0,
            "retain_intersection_validation": 0,
            "forget_intersection_validation": 0,
            "valid": True
        }
        with open(os.path.join(output_dir, "validation_report.json"), "w") as f:
            json.dump(report, f, indent=4)
            
        status.complete()
        print("Splits generated successfully.")
        
    except Exception as e:
        status.fail(e)
        raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    
    generate_splits(args.config, args.overwrite)
