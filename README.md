# Análisis de SBOMs y Vulnerabilidades

Este proyecto automatiza la generación de Software Bill of Materials (SBOM) y el escaneo de vulnerabilidades en repositorios activos de una organización en GitHub.

## Prerrequisitos del Sistema
Para que los scripts de Python funcionen, es necesario instalar los binarios nativos en el sistema operativo:

1. **Instalar Syft:** `curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sudo sh -s -- -b /usr/local/bin`
2. **Instalar Grype:** `curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin`

## Instalación del Entorno
1. Clonar este repositorio.
2. Crear un entorno virtual: `python -m venv .venv`
3. Activar el entorno e instalar dependencias: `pip install -r requirements.txt`
4. Crear un archivo `.env` en la raíz con tu token de GitHub: `GITHUB_TOKEN=tu_token_aqui`

## Ejecución del Análisis
Ejecuta los siguientes comandos desde la raíz del proyecto (`sBOMS/`):

1. **Obtener repositorios activos:** `python scripts/fetch_repos.py`
2. **Generar SBOMs y escanear:** `python scripts/generate_sboms.py`
3. **Ver resultados:** Abre y ejecuta el notebook en `nbs/vuln/generacion_grype.ipynb`.