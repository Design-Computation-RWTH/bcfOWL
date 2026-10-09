#!/usr/bin/env bash
# Build the documentation of every released version into ./docs/<version>/.
# Run after scripts/build-docs.sh, which builds the latest version into ./docs.
# A release is a git tag v<version>, e.g. v1.0.0. Each tag is built with the
# build-docs.sh of that tag, so a published version keeps its exact content.
set -euo pipefail

OUT="docs"

cd "$(dirname "$0")/.."
ROOT="$(pwd)"

test -d "$OUT" || { echo "Run scripts/build-docs.sh first" >&2; exit 1; }
mkdir -p .cache

WORK="$(mktemp -d)"
trap 'for wt in "$WORK"/*; do [ -d "$wt" ] && git worktree remove --force "$wt"; done; rm -rf "$WORK"' EXIT

for tag in $(git tag --list 'v[0-9]*' --sort=version:refname); do
  version="${tag#v}"
  wt="$WORK/$version"
  git worktree add --quiet --detach "$wt" "$tag"

  # The tag must describe the version it is published as.
  if ! grep -q "owl:versionIRI <https://w3id.org/bcfOWL/${version}>" "$wt/ontology/bcfOWL.ttl"; then
    echo "Tag $tag: ontology/bcfOWL.ttl does not declare owl:versionIRI <https://w3id.org/bcfOWL/${version}>" >&2
    exit 1
  fi

  # Share the Widoco download cache with the worktree.
  ln -s "$ROOT/.cache" "$wt/.cache"
  bash "$wt/scripts/build-docs.sh"

  rm -rf "$OUT/$version"
  cp -R "$wt/docs" "$OUT/$version"
  echo "Built $OUT/$version/ from $tag"
done
