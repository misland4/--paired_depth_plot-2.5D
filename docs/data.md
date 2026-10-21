# Data dictionary and author-confirmed interpretation

## Source and provenance

`examples/research_pairs.xlsx` is a byte-for-byte copy of the supplied `Simulated dataset to demo the code(1).xlsx`; its original worksheet name `Simulated dataset` is unchanged. The repository filename is historical and does not establish data provenance. Whether this nine-pair example is simulated or actual measured data remains to be clarified; the author's explicit simulated-data response concerned the separate seven-row density example.

- Source SHA-256: `5aff67627188d3528e64b775abea7a2310dae2312189e4f5dce88d7e9a1717d6`.
- Worksheet: `Simulated dataset`.
- Data range: B2:C10, nine complete control/experiment pairs.
- Supplied data and exported figures: [CC BY 4.0](../LICENSES.md).

## Fields and interpretation

| Field | Excel location | Meaning | Unit/scale |
| --- | --- | --- | --- |
| Control group | B1 header; B2:B10 values | First value of each within-subject pair, plotted in blue | Dimensionless ordinal Lesion score |
| Experiment group | C1 header; C2:C10 values | Second value of the same pair, plotted in green | Dimensionless ordinal Lesion score |
| ID | Generated from input row order | Sequential display ID linking both values in a row | Not a supplied subject identifier |
| Depth | Generated with seed 20260709 | Separates overlapping pairs for display | Not a measured variable |

The author confirms that **each row contains paired samples from the same subject**. Column A is unused. The workbook contains nine pairs; the lack of subject identifiers means the number of distinct subjects across rows is not established.

The formal metric and vertical-axis label are **Lesion score**, a dimensionless ordinal grading. Control values range from 1 to 3 and experiment values from 0 to 2. The authors have not provided the criteria for individual grades 0, 1, 2 and 3; the script does not assign clinical category definitions to them.

## Display calculations

Each pair keeps one shared, reproducible depth offset across both columns. Input row order and the random seed determine only these offsets; scores are unchanged. Lines connect the two values of each row and the vertical range expands to include score 3. No hypothesis test or significance annotation is generated. The authors confirm that the depth dimension is for display only and need not be described as a measured variable in the paper.

## Details deferred until publication

The authors will provide specific treatments, conditions, time points, final English group names, study background/source description and the corresponding paper/figure upon publication. Until then the plot keeps `Control group` and `Experiment group`. The manuscript is unpublished; cite the code repository.

`examples/paired_values.csv` and the built-in ten-pair arrays are a separate historical software example under Apache-2.0. They are not combined with the supplied nine-pair workbook.
