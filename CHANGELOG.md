# Changelog

This file lists the changes to bcfOWL between published versions.

| Version | Date       | Namespace                                | Status    |
| ------- | ---------- | ---------------------------------------- | --------- |
| 1.0.0   | 2026-10-07 | `https://w3id.org/bcfOWL#`               | current   |
| 0.7.1   | 2022-03-16 | `http://lbd.arch.rwth-aachen.de/bcfOWL#` | superseded ([DOI 10.5281/zenodo.4710742](https://doi.org/10.5281/zenodo.4710742)) |

## 1.0.0 (2026-10-07)

**Summary.** bcfOWL is no longer a "one-to-one" copy of the BCF schema. It reuses existing vocabularies for everything that is not specific to BCF, and it keeps only the coordination concepts: Project, Topic, Comment, Viewpoint, and the visual state of a Viewpoint. The ontology has a persistent namespace and a SHACL profile for the structural rules. **Data in the 0.7.1 vocabulary needs a migration.** The tables below show how.

### Breaking changes

- **New namespace.** The namespace is `https://w3id.org/bcfOWL#`. The old namespace `http://lbd.arch.rwth-aachen.de/bcfOWL#` is not used any more. The ontology declares `owl:priorVersion` and `owl:incompatibleWith` for it.
- **Terms were removed or replaced** (see the migration tables).
- **No cardinality restrictions in OWL.** All `owl:cardinality`, `owl:minCardinality` and `owl:maxCardinality` restrictions are removed. Under the open-world assumption, a restriction such as "exactly one title" does not validate. A reasoner would instead infer that two titles are the same individual. The structural rules are now in the SHACL profile [bcfOWL-shapes](https://github.com/Design-Computation-RWTH/bcfOWL-shapes).
- **foaf is no longer used.** Authors and assignees are `prov:Agent`. A person, an organization, or a software agent can take these roles.

### Migration: terms that other vocabularies now cover

| 0.7.1 | 1.0.0 |
| --- | --- |
| `bcfOWL:hasGuid`, `bcfOWL:hasProjectId` | `dcterms:identifier` |
| `bcfOWL:hasTitle` (Topic), `bcfOWL:hasName` (Project) | `dcterms:title` |
| `bcfOWL:hasDescription` (Topic) | `dcterms:description` |
| `bcfOWL:hasCreationAuthor`, `bcfOWL:hasAuthor` (creator of a Topic or Comment) | `dcterms:creator` |
| `bcfOWL:hasCreationDate`, `bcfOWL:hasCommentDate` | `dcterms:created` |
| `bcfOWL:hasTopicModifiedAuthor`, `bcfOWL:hasCommentModifiedAuthor`, `bcfOWL:lastModifiedBy` | `bcfOWL:modifiedBy` (optional shortcut for the latest change) |
| `bcfOWL:hasTopicModifiedDate`, `bcfOWL:hasCommentModifiedDate` | No property. Derive the date from the change history. |
| `bcfOWL:hasIfcElement` | `bcfOWL:hasElement`. The range is `bot:Element` and is not limited to IFC. |

The project user list is new in the extension schema: `bcfOWL:hasUser` lists the agents of a project.

### Migration: camera and viewpoint

| 0.7.1 | 1.0.0 |
| --- | --- |
| `bcfOWL:Camera`, `bcfOWL:PerspectiveCamera`, `bcfOWL:OrthogonalCamera` | A `sosa:Observation`: one capture or view that a `sosa:Sensor` (the physical or virtual camera) makes at a specific pose. The Viewpoint refers to it with `bcfOWL:hasPerspectiveCamera` or `bcfOWL:hasOrthogonalCamera`. The property chosen sets the projection. |
| `bcfOWL:hasCamera` (it was never defined) | `bcfOWL:hasPerspectiveCamera` or `bcfOWL:hasOrthogonalCamera` on the Viewpoint |
| `bcfOWL:hasCameraViewPoint`, `bcfOWL:hasCameraDirection`, `bcfOWL:hasCameraUpVector` | The pose of the observation: a `spot:PointSpace` that represents it, placed with a SPOT appearance and a GOM matrix |
| `bcfOWL:hasSelection`, `bcfOWL:Selection` | No container. The Viewpoint links each selected component directly with `bcfOWL:hasSelectedComponent`. |
| `bcfOWL:hasException`, `bcfOWL:Exception` | No container. The Viewpoint links each component whose visibility differs from the default directly with `bcfOWL:hasVisibilityException`. |
| `bcfOWL:hasLines`, `bcfOWL:Lines` | `bcfOWL:hasLine` and `bcfOWL:Line`, with `bcfOWL:hasStartPoint` and `bcfOWL:hasEndPoint` |
| `bcfOWL:hasClippingPlanes`, `bcfOWL:ClippingPlanes` | `bcfOWL:hasClippingPlane` and `bcfOWL:ClippingPlane`, with `bcfOWL:hasLocation` and `bcfOWL:hasDirection` |
| `bcfOWL:hasTopicsContainer`, `bcfOWL:hasViewpointsContainer`, `bcfOWL:hasCommentsContainer` | Removed. The members of a collection are found with a query. |

### Added

- **Project:** `bcfOWL:referenceSpace` (a `spot:AssetSpace`) states in which coordinate space the BCF API exposes and accepts coordinates.
- **Extension schema:** each category (type, status, label, priority, stage) is a `skos:ConceptScheme`. Its values
  are `skos:Concept`s of the matching bcfOWL class. The schemes are linked with `bcfOWL:hasTypeScheme`,
  `bcfOWL:hasStatusScheme`, `bcfOWL:hasLabelScheme`, `bcfOWL:hasPriorityScheme` and `bcfOWL:hasStageScheme`.
  The Topic value properties now have the domain `bcfOWL:Topic`.
- **Viewpoint:** `bcfOWL:hasSnapshot` (a `dcat:Dataset`), `bcfOWL:hasBitmap` and `bcfOWL:hasBitmapImage`,
  `bcfOWL:hasColoring`, `bcfOWL:hasColor`, and the compact literals `bcfOWL:point3D` and `bcfOWL:vector3D`.
  A Viewpoint can have a camera, a snapshot, or both.
- **Projection parameters:** `bcfOWL:hasFieldOfView`, `bcfOWL:hasAspectRatio` and `bcfOWL:hasViewToWorldScale` on
  the observation. They make a lossless BCF round trip possible. No maintained vocabulary defines them.
- **`bcfOWL:hasIndex`:** orders Topics and Viewpoints.
- **Camera frame:** a right-handed camera frame as in glTF. The view direction is -Z and up is +Y. For a
  column-major GOM matrix M, BCF `camera_view_point` is column 4, `camera_direction` is the normalized negative
  column 3, and `camera_up_vector` is the normalized column 2.
- **Examples** in `examples/`, and a SHACL profile in a separate repository.

### Changed modeling decisions

- **Reuse by IRI, no imports.** bcfOWL uses terms of BOT, SOSA, SKOS, DCTERMS, PROV-O, DCAT and SPOT in its axioms
  but does not import them. It needs none of their axioms, and an import would load their full closure for every user.
- **Change history is data, not vocabulary.** bcfOWL has no properties for history. Current values are asserted
  directly. Earlier values are kept as RDF 1.2 triple terms, with a `prov:Entity` as reifier and PROV-O activities
  (see `examples/04-provenance.ttl`). Static facts are asserted once: `dcterms:identifier`, `dcterms:creator`,
  `dcterms:created`. Mutable facts keep their history: status, priority, type, stage, labels, assignee, due date,
  title, description, and comment text.
- **A Viewpoint does not change after creation.** Only the pose matrix of its observation can be refined.
- **Pictures do not need BCF.** A camera, a pose and a snapshot are described with SOSA, SPOT and DCAT. They exist
  without a Viewpoint. A Viewpoint only refers to them.

### Fixed

- Removed a serialization error: the old Viewpoint was a subclass of `owlapi#Error1`.
- Removed the undefined property `bcfOWL:hasCamera`.

## 0.7.1 (2022-03-16)

Last version in the old namespace. Documentation: <https://lbd.arch.rwth-aachen.de/bcfOWL_V1/index-en.html>.
