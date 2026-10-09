#!/usr/bin/env python3
"""Check the version declared in ontology/bcfOWL.ttl.

  python3 scripts/check-version.py              # on every push and pull request
  python3 scripts/check-version.py --tag v1.1.0 # before a release

Without --tag: if the ontology differs from the latest release tag, its version
must be higher than that release. Changes to the documentation only (widoco/,
README, examples, ...) need no new version.

With --tag: the ontology must declare exactly the version of the tag, and
owl:priorVersion must be the version IRI of the previous release.

The ontologies are compared as RDF graphs, so changes to formatting and Turtle
comments do not count as changes to the ontology.
"""
import argparse
import os
import re
import subprocess
import sys

from rdflib import Graph, Literal, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import OWL, RDF

ONTOLOGY = "ontology/bcfOWL.ttl"
CHANGELOG = "CHANGELOG.md"
VERSION_IRI = "https://w3id.org/bcfOWL/{}"
TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")

GITHUB = os.environ.get("GITHUB_ACTIONS") == "true"
errors = 0


def error(msg):
    global errors
    errors += 1
    print(f"::error file={ONTOLOGY}::{msg}" if GITHUB else f"ERROR: {msg}", file=sys.stderr)


def notice(msg):
    print(f"::notice::{msg}" if GITHUB else msg)


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def parse(data):
    g = Graph()
    g.parse(data=data, format="turtle")
    return g


def header(g):
    """Return (versionInfo, versionIRI, priorVersion) of the owl:Ontology."""
    onts = list(g.subjects(RDF.type, OWL.Ontology))
    if len(onts) != 1:
        sys.exit(f"{ONTOLOGY}: expected one owl:Ontology, found {len(onts)}")
    get = lambda p: g.value(onts[0], p)
    return get(OWL.versionInfo), get(OWL.versionIRI), get(OWL.priorVersion)


def as_tuple(version):
    return tuple(int(x) for x in version.split("."))


def release_tags():
    """Release tags, oldest first."""
    tags = [t for t in git("tag", "--list", "v*").split() if TAG.match(t)]
    return sorted(tags, key=lambda t: as_tuple(t[1:]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tag", help="release tag to check, e.g. v1.1.0")
    tag = ap.parse_args().tag

    with open(ONTOLOGY, encoding="utf-8") as f:
        current = parse(f.read())
    info, iri, prior = header(current)

    # versionInfo and versionIRI must always agree.
    if info is None or iri is None:
        error("The ontology needs owl:versionInfo and owl:versionIRI.")
        return
    version = str(info)
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        error(f'owl:versionInfo "{version}" is not a version number like 1.2.0.')
        return
    if iri != URIRef(VERSION_IRI.format(version)):
        error(f'owl:versionIRI <{iri}> does not match owl:versionInfo "{version}". '
              f"Expected <{VERSION_IRI.format(version)}>.")

    tags = release_tags()

    if tag:
        if not TAG.match(tag):
            error(f"Tag {tag} is not a release tag like v1.2.0.")
            return
        if version != tag[1:]:
            error(f'Tag {tag} but the ontology declares owl:versionInfo "{version}". '
                  f"Delete the tag (git push --delete origin {tag} && git tag -d {tag}), "
                  f"set owl:versionInfo and owl:versionIRI to {tag[1:]}, then tag again.")
        earlier = [t for t in tags if as_tuple(t[1:]) < as_tuple(tag[1:])]
        if earlier:
            expected = URIRef(VERSION_IRI.format(earlier[-1][1:]))
            if prior != expected:
                error(f"owl:priorVersion is <{prior}>. For {tag} it must be the previous release <{expected}>.")
        with open(CHANGELOG, encoding="utf-8") as f:
            if not re.search(rf"^## {re.escape(tag[1:])}\b", f.read(), re.M):
                error(f"{CHANGELOG} has no section '## {tag[1:]}'.")
        if not errors:
            notice(f"Release {tag}: the ontology declares version {version}.")
        return

    # No tag: compare with the latest release.
    if not tags:
        notice("No release tag yet, nothing to compare with.")
        return
    latest = tags[-1]
    released = parse(git("show", f"{latest}:{ONTOLOGY}"))
    if isomorphic(current, released):
        if version != latest[1:]:
            error(f'The ontology is unchanged since {latest}, but declares version "{version}".')
        else:
            notice(f"The ontology is unchanged since {latest}. No release needed.")
        return
    if as_tuple(version) <= as_tuple(latest[1:]):
        error(f'The ontology changed since release {latest}, but owl:versionInfo is still "{version}". '
              f"Set a higher version in owl:versionInfo and owl:versionIRI, and add it to {CHANGELOG}.")
    elif not errors:
        notice(f"The ontology changed since {latest} and declares the new version {version}. "
               f"Release it with the tag v{version} after it is merged into main.")


if __name__ == "__main__":
    main()
    sys.exit(1 if errors else 0)
