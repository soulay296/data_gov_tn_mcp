# data_gov_tn_mcp

Serveur **MCP** (Model Context Protocol) basé sur **FastMCP** exposant les données ouvertes du portail tunisien [data.gov.tn](https://www.data.gov.tn) via l'API CKAN.

Projet développé dans le cadre d'un stage, avec un suivi par sprints (Sprint 0 : infrastructure).

## Fonctionnalités

- Serveur MCP sur transport HTTP via **FastMCP**
- Endpoint de santé `/health`
- Configuration par variables d'environnement (**Pydantic Settings** + `.env`)
- Logging structuré au format **JSON**
- Conteneurisation **Docker** + orchestration **docker-compose**
- Qualité de code avec **pre-commit** (ruff, ruff-format) et **CI**

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Langage | Python ≥ 3.12 |
| MCP | FastMCP (`fastmcp`) |
| API HTTP | mcp/http + uvicorn |
| Client HTTP | httpx |
| Config | pydantic-settings |
| Logging | python-json-logger |
| Qualité | ruff, pre-commit |
| Conteneurisation | Docker, docker-compose |

## Prérequis

- Python ≥ 3.12
- (Optionnel) Docker & Docker Compose
- (Optionnel) Une clé API data.gov.tn — voir `DATAGOV_API_KEY`

## Installation en local

```bash
python -m venv venv
# Windows (Git Bash)
source venv/Scripts/activate
# Linux/macOS
# source venv/bin/activate

pip install -e ".[dev]"
```

## Configuration

Copier le fichier d'environnement puis l'éditer si besoin :

```bash
cp .env.example .env
```

Variables disponibles (voir `config.py`) :

| Variable | Défaut | Description |
|----------|--------|-------------|
| `MCP_HOST` | `0.0.0.0` | Adresse d'écoute du serveur |
| `MCP_PORT` | `8000` | Port d'écoute |
| `MCP_ENV` | `local` | Environnement du serveur MCP |
| `DATAGOV_API_ENV` | `prod` | Environnement de l'API data.gov.tn |
| `DATAGOV_API_BASE_URL` | `https://www.data.gov.tn/api/3` | URL de base CKAN |
| `DATAGOV_API_KEY` | *(vide)* | Clé API data.gov.tn |
| `LOG_LEVEL` | `INFO` | Niveau de log |
| `SENTRY_DSN` | *(vide)* | DSN Sentry (tracing) |
| `ALLOWED_HOSTS` | data.gov.tn, ... | Hôtes autorisés |
| `ALLOWED_ORIGINS` | `*` | Origines CORS |
| `CORS_ENABLED` | `true` | Activation CORS |
| `MAX_PAGE_SIZE` / `MAX_DOWNLOAD_SIZE_MB` | `100` / `100` | Limites pagination / téléchargement |
| `REQUEST_TIMEOUT` | `30` | Timeout des requêtes sortantes (s) |

## Lancement

### En local

```bash
python main.py
```

L'API répond sur `http://localhost:8000`. Test du endpoint de santé :

```bash
curl http://localhost:8000/health
```

Réponse attendue :

```json
{
  "status": "healthy",
  "uptime_since": "2026-01-01T00:00:00+00:00",
  "version": "1.0.0",
  "env": "local",
  "data_env": "prod",
  "timestamp": "..."
}
```

### Avec Docker

```bash
docker compose up --build
```

Le service `mcp-server` est construit à partir du `Dockerfile` et un `healthcheck` vérifie `/health` toutes les 30 s.

## Qualité de code : pre-commit

Les hooks sont définis dans `.pre-commit-config.yaml` :

- `ruff` (lint + auto-fix)
- `ruff-format` (formatage)
- `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-added-large-files`

Installation et exécution :

```bash
pip install pre-commit        # si ce n'est pas déjà le cas
pre-commit install            # installe le hook de commit
pre-commit run --all-files    # exécute sur tout le dépôt
```

Le hook s'exécute automatiquement à chaque `git commit`.

## Tests

```bash
pytest
```

## Structure du projet

```
.
├── main.py                # Entrée du serveur MCP, endpoint /health
├── config.py              # Configuration Pydantic Settings
├── logging_config.py      # Logging structuré JSON
├── pyproject.toml         # Métadonnées, dépendances, outils
├── Dockerfile             # Image du serveur
├── docker-compose.yml     # Orchestration (service + healthcheck)
├── .pre-commit-config.yaml
├── tools/                 # Outils MCP (à venir au Sprint 1)
├── helpers/               # Utilitaires (à venir)
├── models/                # Modèles de données (à venir)
└── tests/                 # Suite de tests
```

## Licence

MIT — voir [LICENSE](LICENSE).
