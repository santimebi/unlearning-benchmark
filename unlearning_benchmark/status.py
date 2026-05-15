import json
import time
import os

class StatusManager:
    def __init__(self, step_name: str, output_dir: str):
        self.step_name = step_name
        self.output_dir = output_dir
        self.status_file = os.path.join(output_dir, "status.json")
        self.start_time = None
        
        # Ensure output dir exists
        os.makedirs(self.output_dir, exist_ok=True)

    def start(self):
        self.start_time = time.time()
        self._write_status("running")

    def complete(self):
        self._write_status("completed")

    def fail(self, exception: Exception):
        self._write_status("failed", error_type=type(exception).__name__, error_message=str(exception))

    def _write_status(self, state: str, error_type: str = None, error_message: str = None):
        duration = time.time() - self.start_time if self.start_time else 0
        status_data = {
            "step": self.step_name,
            "state": state,
            "duration_seconds": duration
        }
        if error_type:
            status_data["error_type"] = error_type
        if error_message:
            status_data["error_message"] = error_message
            
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=4)
