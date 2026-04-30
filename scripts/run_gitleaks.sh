#!/bin/bash

# 1. Actualizar y clonar los repositorios usando tu script de Python
echo "=== Paso 1: Obteniendo y clonando repositorios ==="
python scripts/fetch_repos.py

# 2. Preparar el directorio de resultados limpios
echo "=== Paso 2: Preparando directorio de resultados ==="
mkdir -p data/results/gitleaks_reports
# Limpiamos resultados anteriores para no mezclar datos viejos
rm -f data/results/gitleaks_reports/*.json

# 3. Ejecutar Gitleaks y guardar directamente en la carpeta final con el nombre correcto
echo "=== Paso 3: Ejecutando Gitleaks por repositorio ==="
for repo in data/repos/*; do
  if [ -d "$repo/.git" ]; then
    repo_name=$(basename "$repo")
    echo "Analizando repositorio: $repo_name..."
    # Ejecuta gitleaks y lo guarda ya con el nombre correcto en results
    gitleaks detect --source "$repo" --report-path "data/results/gitleaks_reports/${repo_name}_report.json"
  fi
done

echo "=== ¡Proceso Finalizado! ==="
echo "Los reportes se encuentran en: data/results/gitleaks_reports/"