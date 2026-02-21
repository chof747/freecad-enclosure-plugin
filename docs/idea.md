# Enclosure Automation Tool Idea

I’m looking for a software tool that integrates with KiCad. The tool should:

1. Take an electrical design from KiCad.
2. Use the corresponding 3D model from KiCad.
3. Automatically generate an enclosure around the board.
4. Include screw hole placements aligned with the PCB.
5. Add cutouts for connectors and components that protrude from the board.

This would streamline enclosure design significantly!

## Related Tools & Workflows

1. **TurboCase**: A tool that can generate OpenSCAD enclosures from KiCad data, including screw holes and basic cutouts.
2. **KiCad StepUp (FreeCAD)**: A workbench for FreeCAD that imports KiCad designs for further CAD refinement.
3. **Fusion 360 / FreeCAD Manual Workflow**: Importing the board into a CAD tool, then manually designing the enclosure.

These can serve as inspiration or starting points for building a more automated solution!

## Architecture Mapping

The current capability mapping and extension boundaries are tracked in
`docs/architecture/capability-map.md`.
