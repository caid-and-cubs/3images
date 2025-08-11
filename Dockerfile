# 1. Phase de construction : installation des dépendances
FROM python:3.11-slim-bookworm AS builder

# Copier l’exécutable `uv` depuis l’image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Activer bytecode compilation et copie (pas de liens symboliques)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copier les fichiers de dépendances pour la mise en cache Docker
COPY pyproject.toml uv.lock ./

# Installer uniquement les dépendances (sans installer le projet)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copier le reste du projet et installer les dépendances + Django
COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Exécuter collectstatic dans l’environnement `uv`
RUN uv run python manage.py collectstatic --noinput

# 2. Phase de production : image finale légère
FROM python:3.11-slim-bookworm AS production

WORKDIR /app

# Copier le contenu complet du builder
COPY --from=builder /app /app

# Ajouter l’environnement virtuel `uv` au PATH
ENV PATH="/app/.venv/bin:$PATH"

# Créer un utilisateur non-root pour plus de sécurité
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Migrations puis lancement de l’application via Gunicorn
CMD ["sh", "-c", "uv run python manage.py migrate && uv run gunicorn --bind 0.0.0.0:8000 main:app"]
