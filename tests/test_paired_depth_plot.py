"""Check external paired data and fail clearly on ambiguous pair IDs."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "paired_depth_plot.py"


class PairedPlotTests(unittest.TestCase):
    def run_cli(self, folder, text):
        source = folder / "pairs.csv"
        source.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(source),
             "--output-dir", str(folder / "figures")],
            cwd=folder, env={**os.environ, "MPLBACKEND": "Agg", "PYTHONIOENCODING": "utf-8"},
            capture_output=True, text=True, encoding="utf-8",
        )

    def test_external_pairs_produce_three_formats(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            result = self.run_cli(folder, "ID,control,experiment\na,1,0\nb,2,1\n")
            self.assertEqual(result.returncode, 0, result.stderr)
            for extension in ("png", "pdf", "svg"):
                output = folder / "figures" / f"paired_depth_plot.{extension}"
                self.assertTrue(output.is_file(), str(output))
                self.assertGreater(output.stat().st_size, 100)

    def test_duplicate_ids_report_an_input_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli(Path(tmp), "ID,control,experiment\na,1,0\na,2,1\n")
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("unique", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_research_excel_pairs_produce_three_formats(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input",
                 str(SCRIPT.parent / "examples" / "research_pairs.xlsx"),
                 "--output-dir", str(folder)],
                cwd=folder, env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            for extension in ("png", "pdf", "svg"):
                self.assertGreater((folder / f"paired_depth_plot.{extension}").stat().st_size, 100)


if __name__ == "__main__":
    unittest.main()
