# bcfOWL — BIM Collaboration Format Ontology

bcfOWL represents the [BIM Collaboration Format (BCF)](https://technical.buildingsmart.org/standards/bcf/) in RDF. It composes BCF from established vocabularies (SOSA, SPOT, PROV-O, DCAT, SKOS, Dublin Core) and keeps only the coordination concepts that no other vocabulary covers.

- Namespace: `https://w3id.org/bcfOWL#` (prefix `bcfOWL`)
- Version: 1.0.0
- Source: [`ontology/bcfOWL.ttl`](ontology/bcfOWL.ttl)
- Examples: [`examples/`](examples) (a project, a clash issue with a comment, a viewpoint, change history)
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

The namespace resolves after its w3id redirect is registered.

## Versions

| Version | Namespace                                  | Documentation                                                                 | DOI                                                                  |
| ------- | ------------------------------------------ | ----------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 1.0.0   | `https://w3id.org/bcfOWL#`                 | this repository                                                               | assigned on release                                                  |
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

On GitHub, every push to `main` rebuilds the page and deploys it to GitHub Pages.

## Authors

Oliver Schulz, Jyrki Oraskari, Jakob Beetz — [Design Computation, RWTH Aachen University](https://dc.rwth-aachen.de/)
