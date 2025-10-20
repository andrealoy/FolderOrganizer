# FolderOrganizer/core/json_utils.py
import json
from pathlib import Path


class JSONHandler:
    """
    Handles parsing, cleaning, and saving JSON data
    from GPT folder organization responses.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    # ---- Core parsing ----
    def parse_response(self, response) -> dict:
        """
        Parse the raw GPT response and return a normalized JSON.
        """
        raw_output = getattr(response, "output_text", None)
        if raw_output is None:
            try:
                raw_output = response.output[0].content[0].text
            except Exception as e:
                raise ValueError(f"Unexpected response format: {e}")

        parsed = self._parse_json_flexibly(raw_output)
        parsed = self._normalize_paths(parsed)
        return parsed

    def _parse_json_flexibly(self, raw_output):
        """
        Internal helper to safely decode malformed JSON.
        """
        if not isinstance(raw_output, str):
            return raw_output

        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            cleaned = raw_output.strip().replace("\\n", "").replace("\n", "")
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                raise ValueError("Failed to parse GPT JSON output")

    # ---- Cleaning ----
    def clean_json(self, data: dict) -> dict:
        """
        Clean and print JSON (remove spaces in filenames, normalize paths).
        """
        cleaned = self._clean_data(data)
        if self.verbose:
            print(json.dumps(cleaned, indent=4))
        return cleaned

    def _clean_data(self, data):
        if isinstance(data, dict):
            return {
                k: self._clean_data(v)
                if k not in ["ignore", "unzip"]
                else v
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [self._clean_data(item) for item in data]
        elif isinstance(data, str):
            return self._clean_path(data)
        return data

    # ---- Path utilities ----
    def _normalize_paths(self, data):
        if isinstance(data, dict):
            return {k: self._normalize_paths(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._normalize_paths(v) for v in data]
        elif isinstance(data, str):
            #replace double backslashes and uniformises separators
            return str(Path(data.replace("\\", "/")))
        return data

    def _clean_path(self, path):
        p = Path(path)
        return str(p.with_name(p.name.replace(" ", "")))

    # ---- File I/O ----
    def save(self, data: dict, path: str):
        """
        Save a JSON file to disk.
        """
        output_path = Path(path).resolve()
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        if self.verbose:
            print(f"JSON saved to {output_path}")

    def load(self, path: str) -> dict:
        """
        Load a JSON file from disk.
        """
        output_path = Path(path).resolve()
        with open(output_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if self.verbose:
            print(f"JSON loaded from {output_path}")
        return data
