# 🗂️ Folder Organizer

**Folder Organizer** est un projet Python qui permet de réorganiser automatiquement un dossier à l’aide de GPT.  
Le programme analyse la structure d’un dossier, envoie ces informations à GPT, et reçoit en retour un plan d’organisation au format JSON.  
Il peut ensuite créer les nouveaux dossiers, copier les fichiers, et dézipper les archives automatiquement.

---

## Structure du projet
```
FolderOrganizer/
├── core/
│ ├── gpt_client.py # Communication avec GPT
│ ├── json_utils.py # Nettoyage et parsing du JSON
│ ├── executor.py # Opérations sur le système de fichiers (copie, unzip…)
├── ui/
│ └── streamlit_app.py # Interface utilisateur Streamlit
└── main.py # Point d’entrée en ligne de commande (CLI)
```

### Branches principales
  
main:	Version stable, propre et fonctionnelle	Andrea (merge uniquement quand tout marche)  
dev:	Branche de travail principale (backend + UI)	Andrea & Colline  
playground:	Zone de test libre (prototypes, essais rapides)	  

### Workflow quotidien
### Étape 1 – Se mettre à jour

Avant de commencer à travailler :

```
git checkout dev
git pull origin dev
```

### Étape 2 – Travailler sur ta partie

Andrea → dossiers core (logique, classes, exécution)

Colline → dossier ui (interface Streamlit, intégration des actions)

Fais tes modifications, puis sauvegarde :
```
git add .
git commit -m "update UI"   # ou "improve backend"
```

### Étape 3 – Synchroniser avec la branche commune

Avant de pousser :
```
git pull origin dev   # récupère les changements de l’autre
git push origin dev   # envoie tes changements
```

### Important : toujours pull avant push pour éviter les conflits.

### Étape 4 – Fusionner vers main

Quand tout fonctionne bien et qu’une version est prête :
```
git checkout main
git pull origin main
git merge dev
git push origin main
```

main devient alors la version “stable”.

### Utilisation de playground

Sert à tester du code, des fonctions ou des idées sans impacter dev

Tu peux y créer un fichier temporaire (test_playground.py, etc.)

Rien d’important ne doit y rester longtemps

Pour aller dessus: 
```
git checkout playground 
```

### Bonnes pratiques

Ne jamais travailler directement sur main

Toujours commenter clairement les commits

Avant un push, vérifie que ton code s’exécute sans erreur

Si tu modifies une fonction utilisée par l’autre personne → préviens-la !

Si tu crées un nouveau fichier, ajoute une docstring en haut avec ton nom et le but du script

##  Andrea – Partie "Core"

### Objectif
Créer toute la logique interne (GPT, parsing, création de dossiers, copie, unzip, etc.)

### À faire
- [ ] Implémenter l’unzip dans `Executor`
  - Chaque entrée doit contenir :
    ```json
    { "source": "/path/to/archive.zip", "destination": "/path/to/folder" }
    ```
- [ ] Ajouter la copie de fichiers dans `Executor`
  - Vérifier que la source existe  
  - Copier les fichiers dans le dossier cible  
  - Gérer un mode `dry_run=True` pour tester sans rien copier
- [ ] Vérifier que :
  - `target_path` n’est pas vide ou invalide  
  - `user_path` existe
- [ ] Permettre la création d’une structure même vide :

 Vérifier que les fichiers de "ignore" ne sont pas présents ailleurs dans le JSON.

### Colline – Partie "Interface Streamlit"
###  Objectif
Créer l’interface Streamlit et la connecter aux fonctions du backend.


-élément: 📁 Sélecteur de dossier source	type: Drag & drop ou bouton	variable: user_path	     description: Dossier à organiser  
-élément: 💬 Champ texte	                type: Text area	            variable: user_prompt	 description: Description de l’organisation souhaitée  
-élément: 🎯 Sélecteur de dossier cible	    type: Bouton / file picker	variable: target_path	 description: Dossier de destination  

## Fonctionnement à implémenter dans Streamlit:

### Récupérer les entrées utilisateur

```
user_path = <dossier sélectionné>
user_prompt = <texte saisi>
target_path = <chemin de destination>
```

### Envoyer les infos à GPT
```
rsp = gpt.send_request(user_path, target_path, user_prompt)
parsed = handler.parse_response(rsp)
cleaned = handler.clean_json(parsed)
handler.save(cleaned, "fstructure.json")
st.json(cleaned)
```

### Créer les dossiers quand l’utilisateur clique sur “Créer la structure”
```
if "structure" not in cleaned:
    raise KeyError("Structure manquante dans la réponse GPT")
executor.make_dirs(cleaned["structure"], target_path)
```
### Optionnel : ajouter un bouton pour dézipper
```
if "unzip" in cleaned:
    executor.unzip_files(cleaned["unzip"])

```
### Executer le fichier main.py
```
main.py – Mode développeur (test sans UI)
```
Ce fichier permet de tester tout le pipeline sans Streamlit.
Il exécute les étapes principales : GPT → JSON → création des dossiers.

### Exemple d’utilisation
```
python -m FolderOrganizer.main \
  --user_path "/home/andreal/Documents/Test_directory" \
  --target_path "/home/andreal/Documents/testdir_org" \
  --prompt "Classify them in the most efficient way possible."
```

### Pipeline complet
```
Utilisateur (UI)
   ↓
GPTClient → Génère le JSON d’organisation
   ↓
JSONHandler → Nettoie, sauvegarde, vérifie
   ↓
Executor → Crée les dossiers, copie, dézippe
```
### Commandes utiles
```
streamlit run FolderOrganizer/ui/streamlit_app.py	Lance l’interface
python -m FolderOrganizer.main ...	Lance le programme en ligne de commande
pip install -r requirements.txt	Installe les dépendances
pytest -v	Lance les tests unitaires
```
### Récapitulatif des rôles
Andrea:
Gérer la logique backend : GPT, parsing, exécution.

Vérifier la robustesse des chemins et des copies.

S’assurer que tout peut être appelé depuis l’UI sans erreur.

Colline:
Créer l’interface Streamlit.

Connecter les variables (user_path, user_prompt, target_path) aux fonctions existantes.

Afficher clairement le résultat JSON et les messages d’état.

