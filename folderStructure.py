import streamlit as st
import os

def display_tree(path, level=0):
    items = sorted(os.listdir(path))
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            st.markdown(" " * level * 4 + f"📁 **{item}**")
            display_tree(item_path, level + 1)
        else:
            st.markdown(" " * level * 4 + f"📄 {item}")

# Interface
st.title("📂 Folder Tree Viewer")

root_path = st.text_input("Entrez le chemin du dossier :", ".")
if os.path.exists(root_path):
    display_tree(root_path)
else:
    st.error("Le chemin spécifié n'existe pas.")
