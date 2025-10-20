# FolderOrganizer/core/executor.py
from pathlib import Path

class Executor:
    """
    Handles filesystem operations based on the structured JSON from GPT.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def make_dirs(self, structure: dict, target_path: str):
        """
        Create directories and log actions based on a JSON structure.
        """
        for name, content in structure.items():
            current_dir = Path(target_path) / name
            current_dir.mkdir(parents=True, exist_ok=True)

            if self.verbose:
                print(f"📂 Created: {current_dir}")

            if isinstance(content, dict):
                self.make_dirs(content, current_dir)
            elif isinstance(content, list):
                for f in content:
                    if self.verbose:
                        print(f"➡️ Will place file: {f} -> {current_dir}")
