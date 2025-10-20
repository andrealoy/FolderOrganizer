from openai import OpenAI
from pathlib import Path


class GPTClient: 
    """
    Handles communication with the OpenAI API for folder organization tasks.
    """
    
    def __init__(self, model: str = "gpt-5-nano-2025-08-07"):
        self.client = OpenAI()
        self.model = model
        
    def send_request(self , user_path:str , target_path:str , user_prompt:str) -> object:
        
        """
        Sends a structured prompt to OpenAI describing the folder organization request.

        Args:
            user_path (str): Path to the source folder to organize.
            target_path (str): Path where the organized files will be placed.
            user_prompt (str): Description of how to organize the folder.

        Returns:
            object: Raw OpenAI API response.
        """
        
        folder_structure = [str(p) for p in Path(user_path).rglob('*')]
        
        
        client = self.client
        
         # Send request
         
        response = client.responses.create(
            model=self.model,
            input=f"""
                    You are an AI specialized in folder organization.

                    Your task:
                    Given:
                    - A folder path
                    - The current folder structure
                    - A user prompt describing the organization goal

                    Return ONLY a valid JSON (no explanations, no markdown).

                    The JSON must describe:
                    1. "structure": a hierarchical mapping of folders to lists of file paths. 
                    - You may create subfolders if needed.
                    - If a folder contains subfolders, represent them as nested JSON objects.
                    2. "ignore": list of file paths to ignore (temporary, irrelevant files, etc.)
                    3. "unzip": list of objects, each with:
                    - "source": the path of the zip file to extract
                    - "destination": the folder path where it should be extracted (must be inside {target_path})

                    Rules:
                    - Do not invent non-existent files.
                    - Only include keys that are relevant.
                    - All paths must use forward slashes ("/").
                    - Ensure that "structure" is properly nested and consistent.
                    - If a file is under the "ignore" key , you should make sure it's not present anywhere else. 
                    - Avoid having too generic names for the folders like "files" "trash" etc... you should organize everything depending on the types of files , or user's projects , according to the prompt it gave you.
                    
                    Example of a correct hierarchical "structure":
                    "structure": {{
                    "projects": {{
                        "project_name": [
                        "/path/to/file1.doc",
                        "/path/to/file2.pdf"
                        ],
                        "python_tests": [
                        "/path/to/test_script.py"
                        ]
                    }},
                    "courses": [
                        "/path/to/lesson1.ipynb",
                        "/path/to/lesson2.ipynb"
                    ]
                    }}

                    Input:
                    - Path: {user_path}
                    - Folder structure: {folder_structure}
                    - Context: {user_prompt}
                    - Destination path: {target_path}

                    Output:
                    A single valid JSON object with the structure:

                    {{
                    "structure": {{
                        "<folder_name>": [<file_paths>] or nested objects
                    }},
                    "cleanup": [...],
                    "unzip": [
                        {{
                        "source": "<zip_path>",
                        "destination": "<destination_folder>"
                        }}
                    ]
                    }}
                    """
                    )
    
    
        return response