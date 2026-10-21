# Paired depth plot (2.5D)

[![Reproducibility checks](https://github.com/misland4/--paired_depth_plot-2.5D/actions/workflows/ci.yml/badge.svg)](https://github.com/misland4/--paired_depth_plot-2.5D/actions/workflows/ci.yml)

A Python script for displaying overlapping paired observations with a reproducible display-only depth offset for each pair. The supplied research example contains **9 control/experiment pairs**.

![Paired depth plot generated from the supplied research observations](docs/images/paired_depth_plot.png)

The added depth dimension separates overlapping pairs; it is not a measured variable. Lines connect the two observations in each input row. The script does not perform significance testing.

## Contents

- [System requirements](#1-system-requirements)
- [Installation guide](#2-installation-guide)
- [Demo](#3-demo)
- [Instructions for use](#4-instructions-for-use)
- [Repository contents](#repository-contents)
- [Troubleshooting and support](#troubleshooting-and-support)
- [Data dictionary](docs/data.md)
- [Reproduction record](docs/validation.md)
- [Academic citation](#academic-citation)

## 1. System requirements

### Software dependencies and operating systems

Use **Python 3.13**. The exact tested dependencies are pinned in `requirements.txt`:

| Package | Tested version |
| --- | --- |
| NumPy | 2.3.5 |
| pandas | 2.3.3 |
| Matplotlib | 3.10.6 |
| openpyxl | 3.1.5 |

The verified environment is **Windows 11 Pro, Python 3.13.9**. Other operating systems and Python versions have not been tested for this release. SciPy is not used by this script. Tests use Python's built-in `unittest`, so `pytest` is not required.

### Hardware

A standard desktop CPU is sufficient for these small inputs. No GPU, CUDA, or other non-standard hardware is required. The demo was timed on an Intel Core i5-14600KF desktop with approximately 32 GB RAM; this is the test machine, not a minimum hardware requirement.

## 2. Installation guide

### Windows PowerShell or CMD

```powershell
git clone https://github.com/misland4/--paired_depth_plot-2.5D.git paired_depth_plot-2.5D
cd paired_depth_plot-2.5D
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The clone command supplies a local folder name without the two leading hyphens in the remote repository name. Alternatively, download and extract the repository ZIP, enter its directory, and run the last two commands. No package activation is required.

### macOS/Linux command variant

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Use `.venv/bin/python` in place of `.venv\Scripts\python.exe` in the following commands. These command variants have not been tested on macOS/Linux for this release.

**Measured installation:** creating a new Windows virtual environment took 3.4 seconds, and installing dependencies took 41.6 seconds in one run. Some wheels were cached; network speed and cache state affect these times. See the [reproduction record](docs/validation.md) for details.

## 3. Demo

### Research example

From the repository root, run:

```powershell
.venv\Scripts\python.exe paired_depth_plot.py --input examples/research_pairs.xlsx --output-dir output --seed 20260709
```

Expected files and console output on Windows:

```text
PNG: output\paired_depth_plot.png
SVG: output\paired_depth_plot.svg
PDF: output\paired_depth_plot.pdf
```

The PNG is saved at 300 dpi; PDF and SVG are vector outputs. SVG fonts are converted to paths for portability. The preview above shows the nine supplied pairs, with blue control points and green experiment points. Existing output files with the same names are overwritten.

**Measured runtime:** about **1.3 seconds** for the research example and all three output formats in one run on the test desktop, with dependencies already installed. This is a single-run observation, not a benchmark across machines.

### Data provenance

[Download the included research workbook](examples/research_pairs.xlsx). It is a byte-for-byte copy of the supplied `Simulated dataset to demo the code(1).xlsx`, with a simpler repository filename. The dataset provider confirmed that these are **real research observations**. The original worksheet name, `Simulated dataset`, is retained; the wording in that source name does not reflect the provider's confirmation.

The script reads the nine pairs in `B2:C10` without changing scores or row order. It assigns sequential display IDs because the workbook does not include a subject-ID column.

## 4. Instructions for use

### Use your own Excel workbook

```powershell
.venv\Scripts\python.exe paired_depth_plot.py --input "C:/data/pairs.xlsx" --output-dir "C:/data/figures" --seed 20260709
```

The first worksheet is read using this layout:

| Excel location | Meaning |
| --- | --- |
| B1 | Header: `Control group` |
| C1 | Header: `Experiment group` |
| B2:B... | Control observations |
| C2:C... | Corresponding experiment observations |

Column A is unused. Each row must contain the two observations belonging to the same pair. Entirely blank rows are skipped; half-empty rows and non-finite/non-numeric scores are rejected. Numeric cells or formulas with cached numeric results are required. All complete rows after the headers are read; no fixed nine-row limit is imposed.

### CSV alternative with explicit IDs

```powershell
.venv\Scripts\python.exe paired_depth_plot.py --input "C:/data/pairs.csv" --output-dir output
```

Required columns:

```csv
ID,control,experiment
pair_01,2,1
pair_02,1,1
```

IDs must be non-empty and unique. Each row represents one complete pair. Additional columns are ignored. Pairing is not inferred from separate group files.

### Original built-in example

Running without `--input` retains the ten pairs embedded in the original supplied script:

```powershell
.venv\Scripts\python.exe paired_depth_plot.py --output-dir output_original
```

`examples/paired_values.csv` reproduces those original built-in values. It is a separate historical example and is not the new nine-pair research workbook. Internal `before`/`after` names are retained from that script; displayed group labels are `Control group` and `Experiment group`.

### Plot conventions and reproduction

- First group: **Control group** (blue); second group: **Experiment group** (green).
- Each input pair keeps the same depth position in both groups.
- `--seed` controls only display offsets, not observed scores. Input row order and the seed together determine the depth positions.
- `--output-dir` defaults to `output/` next to the script.
- For scores between 0 and 2, the original vertical scale is retained. Larger or smaller score ranges automatically expand the vertical limits so all observations remain visible.

To reproduce the repository preview, run the research demo with seed `20260709` and the pinned dependencies. Group labels describe the input columns; statistical interpretation depends on the study design.

### Checks

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Repository contents

| Path | Purpose |
| --- | --- |
| `paired_depth_plot.py` | Plotting command-line script |
| `examples/` | Research workbook and separate historical examples |
| `docs/data.md` | Data fields, provenance and interpretation limits |
| `docs/validation.md` | Independent installation/test record |
| `tests/` | Input-validation and complete-output checks |
| `.github/workflows/ci.yml` | Automated tests and demo generation |
| `requirements.txt` | Pinned direct dependencies |
| `requirements-windows-py313.lock.txt` | Complete tested Windows environment |
| `CITATION.cff` | Software citation |
| `CHANGELOG.md` | Version history |

## Troubleshooting and support

- **Wrong input:** check paths, Excel layout and exact column headers. Excel input reads the first worksheet.
- **Missing/non-numeric values:** provide both values per row. Recalculate and save Excel formulas so cached numeric results exist.
- **Cannot write outputs:** close files held open by other applications, or choose a writable `--output-dir`.
- **Installation errors:** select Python 3.13 and install this repository's requirements. See the [tested environment](docs/validation.md).
- **Plot/input constraints:** Depth offsets are display-only. Use the same input order and `--seed` for repeatable placement; CSV IDs must be unique.

Use [GitHub Issues](https://github.com/misland4/--paired_depth_plot-2.5D/issues) to report reproducible problems; see [CONTRIBUTING.md](CONTRIBUTING.md). Known data fields and scientific context still needed from the authors are described in [docs/data.md](docs/data.md).

## Version and validation

Current software version: **1.0.0**. See [CHANGELOG.md](CHANGELOG.md) and [Releases](https://github.com/misland4/--paired_depth_plot-2.5D/releases) for fixed versions. Local clean-environment checks passed. The badge above links to automated checks; consult each platform job for actual passing results.

## Authors

Project creators and lead maintainers:

- Chunying Li, Email: <lichying@fmmu.edu.cn>
- Yinghan Wang, Email: <wang.yinghan@qq.com>

## Credits

We would like to thank Shuo Yang for his assistance with this project.

## Academic citation

Please cite the software using [CITATION.cff](CITATION.cff), or GitHub's **Cite this repository** panel:

Li, C., & Wang, Y. (2026). *Paired depth plot (2.5D)* (Version 1.0.0) [Computer software]. https://github.com/misland4/--paired_depth_plot-2.5D

The associated research-paper citation has not yet been supplied; no article DOI is assumed.

## License

The project contact has confirmed permission to reuse the code and data. The authors have not yet specified a named license or its scope, so no standard license file has been selected. This statement does not assign additional license terms; formal licensing will be added after author confirmation.
