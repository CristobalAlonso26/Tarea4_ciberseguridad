import os
import requests
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

# Cargar variables de entorno (desde la raíz)
load_dotenv()

ORG = "encode"
MAX_REPOS = 50
TOKEN = os.getenv("GITHUB_TOKEN")
RESULTS_DIR = "data/results"
OUTPUT_FILE = os.path.join(RESULTS_DIR, "repos_activos.json")

if not TOKEN:
    raise ValueError("No se encontró GITHUB_TOKEN. Verifica tu archivo .env")

HEADERS = {"Authorization": f"token {TOKEN}"}


def get_active_repos(org, days=30):
    url = f"https://api.github.com/orgs/{org}/repos?per_page=100&type=public"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error en la API: {response.status_code}")
        return []

    repos = response.json()

    if len(repos) > MAX_REPOS:
        print(f"[-] La organización '{ORG}' tiene {len(repos)} repos (máximo {MAX_REPOS}).")
        print("    Selecciona una organización más pequeña.")
        return []

    cutoff = datetime.utcnow() - timedelta(days=days)
    active = []

    for r in repos:
        if not r.get("pushed_at"):
            continue

        pushed = datetime.strptime(r["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
        if pushed >= cutoff:
            active.append({
                "name": r["name"],
                "clone_url": r["clone_url"],
                "language": r["language"],
                "pushed_at": r["pushed_at"]
            })
    return active


if __name__ == "__main__":
    # Asegurar que el directorio de destino exista
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print(f"[*] Buscando repositorios activos en '{ORG}'...")
    repos = get_active_repos(ORG)
    print(f"[+] Se encontraron {len(repos)} repositorios activos.")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(repos, f, indent=2)
    print(f"[+] Lista guardada en {OUTPUT_FILE}")