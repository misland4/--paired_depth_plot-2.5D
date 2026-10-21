# Contributing and reporting problems

Report a reproducible problem through [GitHub Issues](https://github.com/misland4/--paired_depth_plot-2.5D/issues). Include the command, Python and operating-system versions, the error message and a small input you are authorized to share.

Install `requirements.txt` and run these checks before proposing changes:

```text
python -m unittest discover -s tests -v
python paired_depth_plot.py --input examples/research_pairs.xlsx --output-dir output
```

Changes to scientific interpretation, data values, group labels or licensing require information from the authors. Preserve the supplied workbooks when changing code and keep display-only choices separate from observed values. Data fields and workbook hashes are recorded in [docs/data.md](docs/data.md).
