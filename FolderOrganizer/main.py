# FolderOrganizer/main.py
from core.gpt_client import GPTClient
from core.json_utils import JSONHandler
from core.executor import Executor

"""
main.py
--------
CLI entry point for Folder Organizer.
Used by developers to test the complete pipeline (GPT → JSON → Execution)
without the Streamlit UI.
"""

def ask_user_info() -> tuple[str, str, str]:
    user_path = input("Folder to organize: ").strip()
    target_path = input("Destination folder: ").strip()
    user_prompt = input("Describe your organization goal: ").strip()
    return user_path, target_path, user_prompt


def main():
    user_path, target_path, user_prompt = ask_user_info()

    gpt = GPTClient()
    handler = JSONHandler()
    executor = Executor()

    # 1. Send to GPT
    rsp = gpt.send_request(user_path, target_path, user_prompt)

    # 2. Parsing and cleaning
    parsed = handler.parse_response(rsp)
    cleaned = handler.clean_json(parsed)

    # 3. Save
    handler.save(cleaned, "fstructure.json")

    # 4. Folder creation
    if "structure" not in cleaned:
        raise KeyError("Missing 'structure' in GPT response.")
    executor.make_dirs(cleaned["structure"], target_path)


if __name__ == "__main__":
    main()
