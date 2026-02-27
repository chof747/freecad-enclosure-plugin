# Contract Conventions

## Scope

Applies to feature planning artifacts under `specs/*/contracts/` for this repository.

## Convention

- Contracts are documented as in-process command contracts in Markdown.
- The canonical format matches the style used in
  `specs/001-bootstrap-enclosure-workbench/contracts/enclosure-command-contract.md`.
- Do not generate web API specifications (OpenAPI/GraphQL) unless a feature
  explicitly introduces an external HTTP API.

## Rationale

This plugin executes inside FreeCAD and exposes command-layer behavior rather than
network API endpoints. Markdown command contracts align with existing tests,
workbench command wiring, and user macro workflows.
