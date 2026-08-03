# Requirements artifact layout

This directory follows the Work 3 Requirements artifact layout approved by Human Decision
`DEC-WORK3-REQUIREMENTS-ARTIFACT-LAYOUT-2026-08-03-V1`.

directory names do not confer authority. A structured Requirement becomes effective only when its ID, version and
Digest are connected through a validated candidate, Evidence, Human Decision and authority bundle. Existing stage-four
Requirements remain legacy-bound until a separate migration Decision.

| directory | role |
|---|---|
| `definitions/` | immutable structured Requirement definitions |
| `candidates/` | exact manifests proposed for Human judgment |
| `decisions/` | immutable Human Decision Records |
| `evidence/` | validation, review and post-write Evidence |
| `authority/` | effective definition and legacy authority bindings |

The machine-readable schema is under `schemas/requirements/`. Files in these directories must not be treated as
approved merely because of their path or filename.
