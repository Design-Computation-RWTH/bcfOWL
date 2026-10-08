#!/usr/bin/env bash
# Build the bcfOWL documentation page with Widoco into ./docs
# Used locally and by .github/workflows/docs.yml. Requires Java 17+ and curl.
set -euo pipefail

WIDOCO_VERSION="${WIDOCO_VERSION:-1.4.25}"
ONTOLOGY="ontology/bcfOWL.ttl"
OUT="docs"

cd "$(dirname "$0")/.."

JAR=".cache/widoco-${WIDOCO_VERSION}.jar"
if [ ! -s "$JAR" ]; then
  mkdir -p .cache
  curl -fsSL -o "$JAR" \
    "https://github.com/dgarijo/Widoco/releases/download/v${WIDOCO_VERSION}/widoco-${WIDOCO_VERSION}-jar-with-dependencies_JDK-17.jar"
fi

rm -rf "$OUT"
java -jar "$JAR" \
  -ontFile "$ONTOLOGY" \
  -outFolder "$OUT" \
  -confFile widoco/config.properties \
  -getOntologyMetadata \
  -uniteSections \
  -rewriteAll \
  -noPlaceHolderText \
  -excludeProvenance \
  -lang en

# Widoco does not reliably signal failure through its exit code.
test -s "$OUT/index-en.html" || { echo "Widoco produced no index-en.html" >&2; exit 1; }

# Widoco has no option for custom acknowledgments: insert ours at the top of that section.
python3 - "$OUT/index-en.html" widoco/sections/acknowledgments-en.html <<'PY'
import re, sys
page, extra = sys.argv[1], open(sys.argv[2], encoding="utf-8").read()
html = open(page, encoding="utf-8").read()
html, n = re.subn(r'(<div id="acknowledgments">\s*<h2[^>]*>.*?</h2>)', lambda m: m.group(1) + "\n" + extra, html, count=1, flags=re.S)
if n != 1:
    sys.exit("Acknowledgments section not found in " + page)
open(page, "w", encoding="utf-8").write(html)
PY

# Images referenced by the hand-written sections
mkdir -p "$OUT/assets"
cp assets/* "$OUT/assets/"

# Example files linked from the description
cp CHANGELOG.md "$OUT/CHANGELOG.md"
mkdir -p "$OUT/examples"
cp examples/*.ttl "$OUT/examples/"

cp "$OUT/index-en.html" "$OUT/index.html"
rm -f "$OUT/readme.md"
echo "Built $OUT/index.html"
