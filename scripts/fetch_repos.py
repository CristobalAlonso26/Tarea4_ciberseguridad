import os
import requests
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

ORG = "FlowiseAI"
TOKEN = os.getenv("GITHUB_TOKEN")
RESULTS_DIR = "data/results"
REPOS_DIR = "data/repos"
OUTPUT_FILE = os.path.join(RESULTS_DIR, "repos_activos.json")

HEADERS = {"Authorization": f"token {TOKEN}"}


def get_stars(repo):
    return repo.get("stargazers_count", 0)


def get_top_5_repos(org):
    url = f"https://api.github.com/orgs/{org}/repos?per_page=100&type=public"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []

    repos = response.json()
    repos.sort(key=get_stars, reverse=True)
    top_5 = repos[:5]

    active = []
    for r in top_5:
        active.append({
            "name": r["name"],
            "clone_url": r["clone_url"],
            "language": r["language"],
            "stargazers_count": r["stargazers_count"]
        })
    return active


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(REPOS_DIR, exist_ok=True)
    
    print(f"Buscando los 5 repositorios principales de {ORG}...")
    repos = get_top_5_repos(ORG)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(repos, f, indent=2)
    print(f"Se han guardado los metadatos de {len(repos)} repositorios exitosamente en {OUTPUT_FILE}.")

    print("\nIniciando proceso de clonado/actualización de repositorios...")
    for repo in repos:
        repo_name = repo["name"]
        clone_url = repo["clone_url"]
        repo_path = os.path.join(REPOS_DIR, repo_name)

        if os.path.exists(repo_path):
            print(f"El repositorio '{repo_name}' ya existe. Actualizando (git pull)...")
            subprocess.run(["git", "-C", repo_path, "pull"], check=False)
        else:
            print(f"Clonando el repositorio '{repo_name}'...")
            subprocess.run(["git", "clone", clone_url, repo_path], check=False)
            
    print("\nProceso de repositorios finalizado. Listos para análisis con Gitleaks.")
