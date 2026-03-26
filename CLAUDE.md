# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BGI Metadata Editor — a Django-based metadata management system for the WIS-BE project of Canton Bern. It manages geospatial metadata (layers, attributes, value tables) and integrates with ArcGIS Online to create and update web maps.

## Development Setup

```bash
conda create -n bgi_metadata python=3.12
conda activate bgi_metadata
conda install --yes --file requirements.txt
```

Configure a `.env` file (see `.env` for reference — required variables: `SECRET_KEY`, `DEBUG`, `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`).

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver   # http://localhost:8000/
```

## Common Commands

```bash
python manage.py migrate                      # Apply database migrations
python manage.py makemigrations               # Create new migration files
python manage.py test                         # Run tests (editor/tests.py)
python manage.py test editor.tests.TestName   # Run a single test
python manage.py shell                        # Django interactive shell
docker build -t bgi_metadata .                # Build Docker image
```

## Code Style

Follow [PEP 8](https://peps.python.org/pep-0008/) for all Python code. Django's own [coding style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/) applies for conventions specific to Django (models, views, admin). No automated formatter is enforced; consistency with the surrounding code is the guideline.

## Architecture

See [docs/scope_context.svg](docs/scope_context.svg) for the scope and context diagram.

### Project Layout

```
metadata/          # Django project config (settings, root URLs, wsgi)
editor/            # Single Django app containing all business logic
  models/          # One file per model (16 model files)
  views.py         # API endpoints + web map creation views
  admin.py         # Django admin with custom forms and inlines
  urls.py          # App-level URL routing
  templates/       # HTML templates
  migrations/      # Database schema history
  webMap.json      # Template used when creating ArcGIS web maps
```

### Data Model Hierarchy

**Thema → Geopäckli → Ebene / Attribut / Wertetabelle**

- **Thema**: Top-level subject area (topic classification)
- **Geopäckli**: Core metadata container ("geo package") — owns Attribute and Wertetabellen; linked to a Thema
- **Ebene**: Geospatial layer definition (Raster/Vektor/Tabelle); linked to Geopäckli and Dienst; M2M with Attribut, Tags, Triggers, Views
- **Attribut**: Data field descriptor (name, type, constraints); belongs to Geopäckli; M2M with Ebene and Wertetabellen
- **Wertetabelle**: Enumeration/value table; belongs to Geopäckli; M2M with Attribut
- **Dienst**: Web service metadata (AWN/AGI owner, external flag)
- **Webmap**: ArcGIS Online web map config (title, description, culture DE/FR)

Key design decision: Attribute belong to Geopäckli (not Ebene), so they survive layer deletion and can be reused across layers via M2M.

### API Endpoints (editor/views.py)

- `GET /layers/` — JSON list of all Ebene objects
- `GET /layergroups/` — JSON hierarchy of layer groups with their layers
- `POST /savewebmap` — Creates a new ArcGIS Online web map from `webMap.json` template
- `POST /updatewebmap/` — Updates an existing ArcGIS Online item

### ArcGIS Online Integration

The app connects to ArcGIS Online using the `arcgis` Python package with credentials from `.env`. Web map creation reads `editor/webMap.json` as a template, substitutes metadata fields, and calls `gis.content.add()` or `item.update()`.

### Admin Interface

`editor/admin.py` has custom logic to filter the Attribut M2M field on Ebene forms to only show attributes belonging to the selected Geopäckli. This is done via a custom `EbeneAdminForm` with a filtered queryset.

### Deployment

CD pipeline via GitLab CI:
- Push to `dev` → deploys to `bgi-metadata-dev` Kubernetes namespace
- Push to `main` → deploys to `bgi-metadata-prod` Kubernetes namespace

Dockerfile uses a multi-stage Python 3.12-slim build; static files served by WhiteNoise.
