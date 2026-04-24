import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

ORG = "FlowiseAI"
TOKEN = os.getenv("GITHUB_TOKEN")
RESULTS_DIR = "data/results"
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
    print(f"Buscando los 5 repositorios principales de {ORG}...")
    repos = get_top_5_repos(ORG)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(repos, f, indent=2)
    print(f"Se han guardado {len(repos)} repositorios exitosamente.")