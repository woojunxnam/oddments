"""Keep the browser's collection boundary contracts in the normal CI suite."""
from pathlib import Path
import subprocess


def test_verified_law_javascript_contracts():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ['node', '--test', 'tests/test_verified_law_collections.cjs'],
        cwd=root, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
