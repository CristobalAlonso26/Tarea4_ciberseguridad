import os
import requests
from datetime import datetime, timedelta, timezone
import json
from dotenv import load_dotenv

# Cargar variables de entorno (desde la raíz)
load_dotenv()

ORG = "nodejs"
MAX_ACTIVE_REPOS = 50
TOKEN = os.getenv("GITHUB_TOKEN")
RESULTS_DIR = "data/results"
OUTPUT_FILE = os.path.join(RESULTS_DIR, "repos_activos.json")

if not TOKEN:
    raise ValueError("No se encontró GITHUB_TOKEN. Verifica tu archivo .env")

HEADERS = {"Authorization": f"token {TOKEN}"}


def get_all_repos(org):
    """Obtiene todos los repos públicos de la org con paginación."""
    all_repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{org}/repos?per_page=100&type=public&page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Error en la API: {response.status_code}")
            return []

        repos = response.json()
        if not repos:
            break

        all_repos.extend(repos)
        if len(repos) < 100:
            break
        page += 1

    return all_repos


def get_active_repos(org, days=30):
    all_repos = get_all_repos(org)
    print(f"    Total de repos públicos encontrados: {len(all_repos)}")

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    active = []

    for r in all_repos:
        if not r.get("pushed_at"):
            continue

        pushed = datetime.strptime(r["pushed_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if pushed >= cutoff:
            active.append({
                "name": r["name"],
                "clone_url": r["clone_url"],
                "language": r["language"],
                "pushed_at": r["pushed_at"]
            })

    if len(active) > MAX_ACTIVE_REPOS:
        print(f"[-] Se encontraron {len(active)} repos activos (máximo {MAX_ACTIVE_REPOS}).")
        print("    Selecciona una organización con menos actividad reciente.")
        return []

    return active


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print(f"[*] Buscando repositorios activos en '{ORG}'...")
    repos = get_active_repos(ORG)
    print(f"[+] Se encontraron {len(repos)} repositorios activos.")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(repos, f, indent=2)
    print(f"[+] Lista guardada en {OUTPUT_FILE}")
