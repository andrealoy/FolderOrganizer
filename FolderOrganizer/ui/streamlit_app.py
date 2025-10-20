# FolderOrganizer/ui/streamlit_app.py
import streamlit as st

def ask_user_info_ui():
    user_path = st.text_input("Folder to organize")
    target_path = st.text_input("Destination folder")
    user_prompt = st.text_area("Describe your organization goal")
    return user_path, target_path, user_prompt
