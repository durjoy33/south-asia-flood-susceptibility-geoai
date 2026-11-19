#!/usr/bin/env python3
"""Static checks for the public notebook package; does not execute the analysis."""
from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "south_asia_flood_pixel_grouped_spatial_validation.ipynb"


def main() -> None:
    if not NOTEBOOK.exists():
        raise FileNotFoundError(NOTEBOOK)
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code_cells = 0
    output_count = 0
    errors = []
    for i, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        code_cells += 1
        output_count += len(cell.get("outputs", []))
        source = "".join(cell.get("source", []))
        try:
            ast.parse(source)
        except SyntaxError as exc:
            errors.append(f"cell {i}: {exc}")
    if errors:
        raise SystemExit("Notebook syntax errors:\n" + "\n".join(errors))
    if output_count:
        raise SystemExit(f"Notebook contains {output_count} saved outputs; clean outputs before committing.")
    source_text = NOTEBOOK.read_text(encoding="utf-8")
    if "/kaggle/input/datasets/durjoy33/" in source_text:
        raise SystemExit("A user-specific Kaggle input path remains in the notebook.")
    print(f"Notebook static checks passed: {code_cells} code cells, no saved outputs, no hard-coded user Kaggle path.")
    print("This check does not execute raster processing or model fitting.")


if __name__ == "__main__":
    main()
