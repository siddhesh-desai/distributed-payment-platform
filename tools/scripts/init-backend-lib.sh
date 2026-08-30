#!/usr/bin/env bash
# Create a backend lib with uv init, then flatten to match PayFlow layout:
#   libs/backend/<snake_name>/<snake_name>/...
# Folder name == import package name (underscores). No src/ layer.
set -euo pipefail

if [[ $# -lt 1 ]]; then
  cat <<'EOF'
Usage: ./tools/scripts/init-backend-lib.sh <snake_name> [description]

<snake_name> is both the folder and the Python import package (underscores).

Examples:
  ./tools/scripts/init-backend-lib.sh payflow_payments_client
  ./tools/scripts/init-backend-lib.sh payflow_ledger_types "Shared ledger types"
EOF
  exit 1
fi

NAME="$1"
DESC="${2:-PayFlow shared backend library ($NAME)}"
DIR="libs/backend/${NAME}"
DIST_NAME="${NAME//_/-}"

if [[ ! "$NAME" =~ ^[a-z][a-z0-9_]*$ ]]; then
  echo "Invalid name '${NAME}'. Use snake_case starting with a letter (e.g. payflow_common)." >&2
  exit 1
fi

if [[ -e "$DIR" ]]; then
  echo "Already exists: ${DIR}" >&2
  exit 1
fi

# uv init defaults to src/<pkg>/; we flatten to <pkg>/ next to pyproject.toml.
uv init "$DIR" \
  --lib \
  --package \
  --name "$DIST_NAME" \
  --description "$DESC" \
  --vcs none \
  --no-readme \
  --author-from none

# uv derives import name from dist name (hyphens → underscores).
UV_PKG="${DIST_NAME//-/_}"
if [[ "$UV_PKG" != "$NAME" ]]; then
  echo "Expected package dir '${NAME}' but uv created '${UV_PKG}'. Renaming." >&2
  mv "${DIR}/src/${UV_PKG}" "${DIR}/src/${NAME}"
fi

mv "${DIR}/src/${NAME}" "${DIR}/${NAME}"
rmdir "${DIR}/src"

# Flat layout: hatchling packages the top-level package dir (uv_build prefers src/).
cat > "${DIR}/pyproject.toml" <<EOF
[project]
name = "${DIST_NAME}"
version = "0.1.0"
description = "${DESC}"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["${NAME}"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
python_files = ["test_*.py"]
EOF

mkdir -p "${DIR}/tests"
cat > "${DIR}/tests/test_package.py" <<EOF
"""Smoke test for the ${NAME} package root."""


def test_package_importable() -> None:
    import ${NAME}  # noqa: F401
EOF

cat > "${DIR}/project.json" <<EOF
{
  "name": "${NAME}",
  "\$schema": "../../../node_modules/nx/schemas/project-schema.json",
  "projectType": "library",
  "sourceRoot": "libs/backend/${NAME}/${NAME}",
  "tags": ["scope:backend", "type:lib"],
  "targets": {
    "test": {
      "executor": "nx:run-commands",
      "options": {
        "command": "uv run --directory libs/backend/${NAME} pytest",
        "cwd": "{workspaceRoot}"
      }
    },
    "lint": {
      "executor": "nx:run-commands",
      "options": {
        "command": "uv run --directory libs/backend/${NAME} ruff check .",
        "cwd": "{workspaceRoot}"
      }
    },
    "fmt": {
      "executor": "nx:run-commands",
      "options": {
        "command": "uv run --directory libs/backend/${NAME} ruff format .",
        "cwd": "{workspaceRoot}"
      }
    }
  }
}
EOF

echo
echo "Created ${DIR}/ (import: ${NAME}, dist: ${DIST_NAME})."
echo "Next: nx run workspace:sync"
