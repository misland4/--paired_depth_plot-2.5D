# Research data dictionary

## Source and provenance

The project contact confirmed that `examples/research_pairs.xlsx` contains real research observations and that reuse is permitted. A named data license and its detailed scope have not yet been specified by the authors.

The workbook is a byte-for-byte copy of the supplied `Simulated dataset to demo the code(1).xlsx`; the original worksheet name `Simulated dataset` is retained. The historical source name is not used to classify the observations as synthetic.

- Source SHA-256: `5aff67627188d3528e64b775abea7a2310dae2312189e4f5dce88d7e9a1717d6`.
- Worksheet: `Simulated dataset`.
- Data range: B2:C10, nine complete control/experiment pairs.

## Fields and interpretation

| Field | Excel location | Meaning used by the code | Recorded unit |
| --- | --- | --- | --- |
| Control group | B1 header; B2:B10 values | First value of each pair, plotted in blue | Numeric score; scale and units were not supplied |
| Experiment group | C1 header; C2:C10 values | Second value of each pair, plotted in green | Numeric score; scale and units were not supplied |
| ID | Generated from input row order | Sequential display ID linking both values in a row | Not a supplied subject identifier |
| Depth | Generated with seed 20260709 | Separates overlapping pairs for display | Not a measured variable |

Column A is unused. Pairing follows the workbook's row layout. The code does not establish whether two values come from the same subject, matched subjects or another pairing design; that scientific pairing criterion must be supplied by the authors.

The supplied control values range from 1 to 3, and the experiment values range from 0 to 2. The workbook does not define what scores 0, 1, 2 or 3 mean. The code displays numeric values without assuming a clinical, ordinal or measurement scale.

## Display calculations

Each pair keeps one shared, reproducible depth offset across both columns. Input row order and the random seed determine only those offsets. Scores are unchanged. Lines connect the two values of each row; the vertical range expands to include score 3. No hypothesis test or significance annotation is generated.

## Research context awaiting author information

The supplied files do not specify the study/sample population, group/condition definitions, pairing criterion, score definitions/units, number of subjects or associated paper/figure. These fields will be added from the authors' description; they are not inferred from the numbers or from the display IDs.

`examples/paired_values.csv` and the built-in ten-pair arrays are a separate historical example. They are not combined with the nine-pair research workbook.
