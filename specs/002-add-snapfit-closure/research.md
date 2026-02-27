# Phase 0 Research - Snap-Fit Closing Mechanism

## Decision 1: Closing mechanism persistence model

- **Decision**: Represent closing mechanism as a stable string enum (`none`, `snap_fit`) with mechanism-specific parameter payload and version metadata for forward compatibility.
- **Rationale**: Stable string IDs avoid ordinal drift, support future mechanism additions, and preserve backward compatibility for saved models.
- **Alternatives considered**:
  - Integer enum values (rejected: brittle persistence when adding/reordering values)
  - Flat optional fields for all mechanism types (rejected: sparse schema and validation ambiguity)

## Decision 2: Snap-fit geometry strategy

- **Decision**: Use cantilever-style snap-fit tabs/hooks as the initial snap-fit mechanism style, with explicit defaults and bounded parameter ranges.
- **Rationale**: Cantilever snaps are printable in common enclosure workflows and naturally support reversible open/close behavior.
- **Alternatives considered**:
  - Annular/ring snaps (rejected: harder printability/tuning)
  - Living hinges as closure (rejected: fatigue risk and different feature semantics)

## Decision 3: Validation policy (clamp vs fail)

- **Decision**: Apply deterministic validation outcomes:
  - Clamp out-of-range tunable parameters to nearest valid value and continue generation with explicit warnings.
  - Block generation with explicit errors when no valid snap-fit geometry can be produced after clamping.
- **Rationale**: Preserves user productivity for safe corrections while preventing silent creation of invalid/unreversible geometry.
- **Alternatives considered**:
  - Fail on all out-of-range values (rejected: too disruptive)
  - Clamp everything and never fail (rejected: risks invalid geometry acceptance)

## Decision 4: Backward-compatible mode switching

- **Decision**: Switching mechanism from `snap_fit` to `none` suppresses closure geometry but preserves the last snap-fit parameter values for restoration when `snap_fit` is reselected.
- **Rationale**: Avoids loss of user tuning while keeping `none` behavior explicit and non-destructive.
- **Alternatives considered**:
  - Reset parameters on switch to `none` (rejected: destroys user intent)
  - Prompt on every switch (rejected: unnecessary interaction overhead)

## Decision 5: Performance and quality guardrails

- **Decision**: Maintain existing create/update performance thresholds for default-sized models and enforce lint/docstring/FreeCAD smoke checks through existing quality gates.
- **Rationale**: Feature should extend behavior without regressing baseline responsiveness or maintainability standards.
- **Alternatives considered**:
  - Relax performance expectations for first iteration (rejected: creates avoidable regression risk)
  - Add separate tooling stack for this feature (rejected: conflicts with reuse-first and uv-based workflow)
