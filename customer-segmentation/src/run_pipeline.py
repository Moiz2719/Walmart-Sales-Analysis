"""Execute cleaning, clustering, segment profiling, and visualisation."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    ROOT / "src" / "clean_data.py",
    ROOT / "src" / "segment_customers.py",
    ROOT / "src" / "analyze_segments.py",
    ROOT / "src" / "create_visualizations.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n===== Running {script.name} =====", flush=True)
        subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)
    print("\nPipeline complete. Review the tables and charts in outputs/.")


if __name__ == "__main__":
    main()
