import os
import json
import subprocess
import shutil
from git import Repo

# Rutas
REPOS_JSON = "data/results/repos_activos.json"
REPOS_DIR = "data/repos"
SBOMS_DIR = "data/results/sboms"
VULNS_DIR = "data/results/vulns"
SAST_DIR = "data/results/sast"

# Crear directorios
for directory in [REPOS_DIR, SBOMS_DIR, VULNS_DIR, SAST_DIR]:
    os.makedirs(directory, exist_ok=True)


def procesar_repositorios():
    if not os.path.exists(REPOS_JSON):
        print(f"[-] No se encontró {REPOS_JSON}. Ejecuta fetch_repos.py primero.")
        return

    with open(REPOS_JSON, "r") as f:
        repos = json.load(f)

    for repo in repos:
        name = repo["name"]
        clone_url = repo["clone_url"]

        repo_path = os.path.join(REPOS_DIR, name)
        sbom_path = os.path.join(SBOMS_DIR, f"{name}_sbom.json")
        vuln_path = os.path.join(VULNS_DIR, f"{name}_vuln.json")

        print(f"\n[*] Procesando: {name}")

        # 1. Clonar (solo si no existe)
        if not os.path.exists(repo_path):
            print("    -> Clonando repositorio...")
            Repo.clone_from(clone_url, repo_path)

        # 2. Generar SBOM
        print("    -> Generando SBOM (Syft)...")
        syft_cmd = ["syft", f"dir:{repo_path}", "-o", "json"]
        with open(sbom_path, "w") as sbom_file:
            subprocess.run(syft_cmd, stdout=sbom_file, check=True, stderr=subprocess.DEVNULL)

        # 3. Escanear Vulnerabilidades
        print("    -> Escaneando vulnerabilidades (Grype)...")
        grype_cmd = ["grype", f"sbom:{sbom_path}", "-o", "json"]
        with open(vuln_path, "w") as vuln_file:
            subprocess.run(grype_cmd, stdout=vuln_file, check=True, stderr=subprocess.DEVNULL)

        # 4. Análisis estático del código fuente (Semgrep)
        print("    -> Escaneando código fuente (Semgrep)...")
        sast_path = os.path.join(SAST_DIR, f"{name}_sast.json")
        semgrep_cmd = ["semgrep", "scan", "--config", "auto", "--json", repo_path]
        with open(sast_path, "w") as sast_file:
            subprocess.run(semgrep_cmd, stdout=sast_file, check=False, stderr=subprocess.DEVNULL)

        # 5. Limpieza agresiva de disco
        print("    -> Limpiando disco...")
        shutil.rmtree(repo_path, ignore_errors=True)

    print("\n[+] ¡Análisis completado!")


if __name__ == "__main__":
    procesar_repositorios()