# Análisis de Seguridad en la Cadena de Suministro (SAST, SCA y CI/CD)

**Autores:** Cristobal Ramos - Leonardo Castellón

Este proyecto automatiza la evaluación del estado de seguridad de la organización **FlowiseAI** en GitHub mediante el análisis de sus repositorios más relevantes. El análisis cubre tres dimensiones clave exigidas:

1. **Código Fuente (SAST):** Búsqueda de vulnerabilidades directas en el código mediante análisis estático utilizando CodeQL.
2. **Dependencias (SCA):** Generación de inventarios de software (SBOMs) con Syft y escaneo de componentes vulnerables o desactualizados con Grype.
3. **Configuraciones CI/CD:** Revisión automatizada de los workflows de GitHub Actions para detectar configuraciones riesgosas, permisos excesivos y uso de componentes no confiables.

## Prerrequisitos del Sistema

Para que los scripts de Python funcionen correctamente, es necesario instalar los binarios nativos de las herramientas de seguridad en el sistema operativo:

### 1. Instalar CodeQL CLI (Análisis SAST)
Descarga y configura CodeQL para el análisis de código fuente:
```bash
wget https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip
mkdir -p $HOME/codeql-home
unzip codeql-linux64.zip -d $HOME/codeql-home
export PATH=$HOME/codeql-home/codeql:$PATH
```
*(Opcional pero recomendado: añadir `export PATH=$HOME/codeql-home/codeql:$PATH` a tu `~/.bashrc` o `~/.zshrc`)*

### 2. Instalar Syft (Generador de SBOM)
```bash
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sudo sh -s -- -b /usr/local/bin
```

### 3. Instalar Grype (Escáner de Vulnerabilidades SCA)
```bash
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin
```

## Instalación del Entorno Python

1. Clonar este repositorio.
2. Crear un entorno virtual: `python3 -m venv .venv`
3. Activar el entorno:
   - Linux/macOS: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
4. Instalar las dependencias de Python: `pip install -r requirements.txt`
5. Crear un archivo `.env` en la raíz del proyecto con tu token personal de GitHub (necesario para consumir la API y obtener los repositorios):
   ```env
   GITHUB_TOKEN=tu_token_aqui
   ```

## Ejecución del Análisis

Ejecuta los siguientes comandos desde la raíz del proyecto para automatizar la extracción de datos y el análisis de seguridad:

1. **Obtener repositorios activos de la organización:**
   ```bash
   python scripts/fetch_repos.py
   ```

2. **Ejecutar Análisis de Código Fuente (SAST) con CodeQL:**
   ```bash
   python scripts/generate_codeql.py
   ```

3. **Generar SBOMs, Análisis de Dependencias (SCA) y workflows (CI/CD):**
   ```bash
   python scripts/generate_sboms.py
   ```

4. **Ver resultados, métricas y conclusiones:**
   Abre e inicia tu entorno de Jupyter/Notebook. Navega y ejecuta todas las celdas del archivo `nbs/vuln/analisis_vulnerabilidades_flowise.ipynb` para visualizar el análisis consolidado de las tres dimensiones y exportar los datasets en formato `.csv`.