# bcfOWL — BIM Collaboration Format Ontology

bcfOWL represents the [BIM Collaboration Format (BCF)](https://technical.buildingsmart.org/standards/bcf/) in RDF. It composes BCF from established vocabularies (SOSA, SPOT, PROV-O, DCAT, SKOS, Dublin Core) and keeps only the coordination concepts that no other vocabulary covers.

- Namespace: `https://w3id.org/bcfOWL#` (prefix `bcfOWL`)
- Version: 1.0.0
- Source: [`ontology/bcfOWL.ttl`](ontology/bcfOWL.ttl)
- Examples: [`examples/`](examples) (a project, a clash issue with a comment, a viewpoint, change history)
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

The namespace resolves after its w3id redirect is registered. The redirect rules are maintained in [perma-id/w3id.org](https://github.com/perma-id/w3id.org) under `ids/bcfOWL/`.

## Versions

| Version | Namespace                                  | Documentation                                                                 | DOI                                                                  |
| ------- | ------------------------------------------ | ----------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 1.0.0   | `https://w3id.org/bcfOWL#`                 | <https://w3id.org/bcfOWL/1.0.0>                                               | assigned on release                                                  |
| 0.7.1   | `http://lbd.arch.rwth-aachen.de/bcfOWL#`   | [bcfOWL_V1](https://lbd.arch.rwth-aachen.de/bcfOWL_V1/index-en.html)          | [10.5281/zenodo.4710742](https://doi.org/10.5281/zenodo.4710742)     |

The ontology states the previous version with `owl:priorVersion`. Data that uses 0.7.1 terms needs a migration. The changes and a migration table are in [`CHANGELOG.md`](CHANGELOG.md).

## Related repositories

- [bcfOWL-shapes](https://github.com/Design-Computation-RWTH/bcfOWL-shapes): the SHACL profile that checks the BCF structure of a dataset.
- [bcfOWL-demonstrator](https://github.com/Design-Computation-RWTH/bcfOWL-demonstrator): the   competency questions on an example dataset, with a query workbench.

## Building the documentation

Requires Java 17+ and curl. Widoco is downloaded to `.cache/` on first run.

```
bash scripts/build-docs.sh
python3 -m http.server -d docs 8000   # then open http://localhost:8000
```

View the page through a local web server, not by opening `docs/index.html` directly: from `file://` the browser blocks the dark-mode toggle script (CORS error).

Ontology metadata (title, authors, version, dates, license, previous version) comes from the Turtle file. Introduction, description, and acknowledgments are maintained in `widoco/`. The texts in `widoco/sections/` are drafts.

On GitHub, every push to `main` rebuilds the page and deploys it to GitHub Pages:

- `docs/` is the latest version, built from `main`. It is served at `https://w3id.org/bcfOWL`.
- `docs/<version>/` is a released version, built from the git tag `v<version>` by `scripts/build-versions.sh`. It is served at `https://w3id.org/bcfOWL/<version>`, the `owl:versionIRI` of that version.

Each tag is built with the build script of that tag, so a published version does not change. The git tags are the archive of the old versions: do not delete or move a release tag.

## What needs a release

| Change | Release needed? |
| ------ | --------------- |
| `ontology/bcfOWL.ttl`: any change to the RDF (terms, axioms, labels, comments, metadata) | **Yes.** Set a new version in the same pull request. |
| `ontology/bcfOWL.ttl`: only formatting or `#` comments | No |
| Documentation texts (`widoco/`), `README.md`, examples, images, build scripts | No. Merge into `main`. |

A documentation change appears on the latest page (`https://w3id.org/bcfOWL`) after the merge. The pages of released versions (`https://w3id.org/bcfOWL/<version>`) keep the text they had at their release.

`scripts/check-version.py` enforces this on every push and pull request. It compares the ontology with the latest release tag as an RDF graph. If the ontology changed but `owl:versionInfo` is not higher than the released version, the check fails.

## Releasing a version

1. In a pull request, change `ontology/bcfOWL.ttl`:
   - `owl:versionInfo "X.Y.Z"` and `owl:versionIRI <https://w3id.org/bcfOWL/X.Y.Z>`
   - `owl:priorVersion` to the version IRI of the previous release

   Add a section `## X.Y.Z (date)` to `CHANGELOG.md`, and update the table above. Merge the pull request into `main`.
2. Tag the merge commit on `main` and push it:
   ```
   git checkout main && git pull
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
3. The `release` workflow checks the tag. The ontology must declare exactly version `X.Y.Z`, `owl:priorVersion` must be the previous release, and `CHANGELOG.md` must have a section for `X.Y.Z`. If a check fails, no release is created. Delete the tag (`git push --delete origin vX.Y.Z && git tag -d vX.Y.Z`), fix the problem, and tag again.
4. If the checks pass, the workflow creates the GitHub release, with the `CHANGELOG.md` section as release notes. With the Zenodo GitHub integration enabled, Zenodo archives the release and assigns a DOI (metadata from `.zenodo.json`).
5. Then the workflow starts the `docs` workflow on `main`. It publishes the documentation of the release, and `https://w3id.org/bcfOWL/X.Y.Z` resolves.

## Authors

Oliver Schulz, Jyrki Oraskari, Jakob Beetz — [Design Computation, RWTH Aachen University](https://dc.rwth-aachen.de/)
