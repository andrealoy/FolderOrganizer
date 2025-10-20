"""
Global integration test for FolderOrganizer.
Simulates a full run with GPT + JSONHandler + Executor.
"""

from FolderOrganizer.core.gpt_client import GPTClient
from FolderOrganizer.core.json_utils import JSONHandler
from FolderOrganizer.core.executor import Executor

def run_global_test():
    user_path = "/home/andreal/Documents/Test_directory"
    target_path = "/home/andreal/Documents/testdir_org"
    user_prompt = "Classify them in the most efficient way possible. In here we have some houdini projects as well as personal projects , my resume and school sql and data projects I'm currently working on. "
    j_path = "fstructure.json"

    print("🚀 Running FolderOrganizer integration test...")

    gpt = GPTClient()
    handler = JSONHandler()
    executor = Executor()

    # Étape 1 : Appel GPT
    rsp = gpt.send_request(user_path, target_path, user_prompt)

    # Étape 2 : Parsing et nettoyage
    parsed = handler.parse_response(rsp)
    cleaned = handler.clean_json(parsed)

    # Étape 3 : Sauvegarde
    handler.save(cleaned, j_path)

    # Étape 4 : Rechargement et création de dossier
    loaded_json = handler.load(j_path)

    if "structure" not in loaded_json:
        raise KeyError("❌ Missing 'structure' in GPT response.")

    executor.make_dirs(loaded_json["structure"], target_path)
    print("✅ Test completed successfully!")


if __name__ == "__main__":
    run_global_test()
