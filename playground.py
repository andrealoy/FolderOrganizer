"""
This is a playground test file for Folder organizer.
Currently : 
-Checking OpenAI API connection. 

"""


# API CONNECT
from pathlib import Path
from openai import OpenAI
import json 
import time 
import os 

def ask_user_info() -> str: 
    
    user_path = input("What folder should we organize ? :")
    target_path = input("Where should we put the new file ?")
    user_prompt = input("What's the purpose and how should we organize it ? :")
    return user_path , target_path , user_prompt

def send_request(user_path:str , target_path , user_prompt) -> object:
   
    folder_structure = [str(p) for p in Path(user_path).rglob('*')]
    
    
    client = OpenAI()
    
    response = client.responses.create(
        model="gpt-5-nano-2025-08-07",
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
 
 
def normalize_paths(data):
    if isinstance(data, dict):
        return {k: normalize_paths(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_paths(v) for v in data]
    elif isinstance(data, str):
        # remplace les double backslashes et uniformise les séparateurs
        return str(Path(data.replace("\\", "/")))
    else:
        return data
    
       
def mk_json(response: object) -> dict:
    raw_output = getattr(response, "output_text" , None)
    if raw_output is None: 
        try:
            raw_output = response.output[0].content[0].text
        except Exception as e:
            
            raise ValueError(f"Unexpected response format: {e}")
    # Étape 1 : si c’est une chaîne, on essaye de décoder une première fois
    if isinstance(raw_output, str):
        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            # first clean
            cleaned = raw_output.strip().replace("\\n", "").replace("\n", "")
            parsed = json.loads(cleaned)
    else:
        parsed = raw_output

    # if we do have a secondary string inside
    if isinstance(parsed, str):
        try:
            parsed = json.loads(parsed)
        except json.JSONDecodeError:
            print("Second parsing not possible")
        
    parsed = normalize_paths(parsed)
   
    return parsed
    
def clean_path(path):
    if isinstance(path,str):
        p = Path(path)
        new_name = p.name.replace(" " , "")
        return str(p.with_name(new_name))
    return path

def clean_data(data): 
    if isinstance(data,dict):
        return {k : clean_data(v) if k not in ["cleanup" , "unzip"] else v for k,v in data.items()}
    elif isinstance(data,list): 
        return [clean_data(item) for item in data]
    else:
        return clean_path(data)
    
def clean_json(data):
    cleaned_data = clean_data(data)
    print(json.dumps(cleaned_data,indent=4))
    return cleaned_data

def save_json(data,path):
    # save to disk
    output_path = Path(path).resolve()
    with open(output_path, "w") as file:
        json.dump(data, file, indent=2)
        
def load_json(path):
    # load_from_disk
    output_path = Path(path).resolve()
    with open(output_path, "r") as file:
        return json.load(file)
                
def make_dirs(structure, target_path):
    for name , content in structure.items():
        current_dir = Path(target_path) / name
        if not current_dir.exists():
            current_dir.mkdir(parents=True,exist_ok=True)
            print(f"Created {current_dir}")
        if isinstance(content,dict): 
            make_dirs(content,current_dir)
        elif isinstance(content, list): 
            for f in content:
                print(f"Will place file: {f} -> {current_dir}")
            
            
      

        

########## TESTING ##########
user_path = "/home/andreal/Documents/Test_directory"
target_path = "/home/andreal/Documents/testdir_org"
# user_prompt = "It's a directory containing multiple stuff that I downloaded. there's a personal project , some tests with datasets , some tests with houdini and some courses I'm following. I would like a clean folder structure to be efficient."
user_prompt = "Classify them in the most efficient way possible."
j_path="fstructure.json"

########## MAIN ##########
if __name__ == "__main__":
    rsp = send_request(user_path, target_path, user_prompt)
    parsed = mk_json(rsp)
    d = clean_json(parsed)
    if "structure" not in d:
        raise KeyError("""Missing 'structure" in GPT response""")
    save_json(d,j_path)
    loaded_json = load_json(j_path)
    make_dirs(loaded_json["structure"],target_path)


########## IDEAS ##########
##Voir si un print(os.walk(dirpath)) peut mieux marcher
##utiliser pathlib
