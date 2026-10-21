"""A reproducible 2.5D display of overlapping paired observations.

Authors: Chunying Li <lichying@fmmu.edu.cn>, Yinghan Wang <wang.yinghan@qq.com>
Credits: Shuo Yang
"""
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import BadZipFile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager


BEFORE = [1, 1, 1, 2, 1, 1, 1, 2, 1, 1]
AFTER = [0, 1, 1, 1, 1, 0, 0, 1, 1, 0]
BEFORE_COLOR = "#343D8F"
AFTER_COLOR = "#35915B"
LINE_COLOR = "#949CA7"


def configure_fonts() -> None:
    """Prefer an installed Chinese font while keeping portable fallbacks."""
    installed = {font.name for font in font_manager.fontManager.ttflist}
    candidates = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["font.sans-serif"] = [
        name for name in candidates if name in installed
    ]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["svg.fonttype"] = "path"


def build_long_data(input_path: Path | None = None) -> pd.DataFrame:
    """Read complete pairs or retain the supplied script's original values."""
    if input_path is None:
        data = pd.DataFrame({"ID": np.arange(1, len(BEFORE) + 1),
                             "before": BEFORE, "after": AFTER})
    elif input_path.suffix.lower() == ".xlsx":
        data = pd.read_excel(input_path, sheet_name=0, usecols="B:C", engine="openpyxl")
        if list(data.columns) != ["Control group", "Experiment group"]:
            raise ValueError("Excel cells B1/C1 must be Control group / Experiment group.")
        data = data.dropna(how="all").rename(
            columns={"Control group": "before", "Experiment group": "after"})
        data.insert(0, "ID", np.arange(1, len(data) + 1))
    elif input_path.suffix.lower() == ".csv":
        data = pd.read_csv(input_path, dtype={"ID": str})
        if not {"ID", "control", "experiment"}.issubset(data.columns):
            raise ValueError("CSV columns must include ID,control,experiment.")
        data = data[["ID", "control", "experiment"]].rename(
            columns={"control": "before", "experiment": "after"})
    else:
        raise ValueError("Input must be an .xlsx research workbook or a .csv paired table.")
    if data.empty:
        raise ValueError("Input must contain at least one complete pair.")
    if data["ID"].isna().any() or data["ID"].astype(str).str.strip().eq("").any():
        raise ValueError("Every pair must have a non-empty ID.")
    data["ID"] = data["ID"].astype(str).str.strip()
    if data["ID"].duplicated().any():
        raise ValueError("Pair IDs must be unique (one CSV row per pair).")
    for column in ("before", "after"):
        try:
            data[column] = pd.to_numeric(data[column], errors="raise")
        except (TypeError, ValueError) as exc:
            raise ValueError("Paired scores must be numeric.") from exc
    if not np.isfinite(data[["before", "after"]].to_numpy(dtype=float)).all():
        raise ValueError("Paired scores must be finite; missing values are not allowed.")
    return data.melt(
        id_vars="ID",
        value_vars=["before", "after"],
        var_name="Time",
        value_name="Score",
    )


def assign_depth_positions(
    data: pd.DataFrame, seed: int = 20260709
) -> pd.DataFrame:
    """Assign one reproducible display-only depth position to each ID."""
    result = data.copy()
    ids = result["ID"].unique()
    rng = np.random.default_rng(seed)
    base_depths = np.linspace(-0.48, 0.48, len(ids))
    offsets = rng.uniform(-0.018, 0.018, len(ids))
    depth_map = dict(zip(ids, base_depths + offsets))
    result["Depth"] = result["ID"].map(depth_map)
    return result


def create_figure(data: pd.DataFrame):
    """Build the 2.5D paired chart and return its figure and axis."""
    configure_fonts()
    figure = plt.figure(figsize=(9.2, 6.4), facecolor="white")
    axis = figure.add_subplot(111, projection="3d")

    for individual_id, pair in data.groupby("ID"):
        ordered = pair.set_index("Time").loc[["before", "after"]]
        axis.plot(
            [0, 1],
            [ordered["Depth"].iloc[0], ordered["Depth"].iloc[1]],
            ordered["Score"].to_numpy(),
            color=LINE_COLOR,
            linewidth=1.1,
            alpha=0.58,
            zorder=2,
        )

    for time, x_position, color in (
        ("before", 0, BEFORE_COLOR),
        ("after", 1, AFTER_COLOR),
    ):
        subset = data[data["Time"] == time]
        axis.scatter(
            np.full(len(subset), x_position),
            subset["Depth"],
            subset["Score"],
            s=76,
            color=color,
            edgecolor="white",
            linewidth=0.9,
            alpha=0.96,
            depthshade=False,
            zorder=3,
        )

    axis.set_xlim(-0.18, 1.18)
    axis.set_ylim(-0.58, 0.58)
    low, high = float(data["Score"].min()), float(data["Score"].max())
    if low >= 0 and high <= 2:
        axis.set_zlim(-0.18, 2.25)
        axis.set_zticks([0, 0.5, 1, 1.5, 2])
    else:
        padding = max((high - low) * 0.12, 0.25)
        axis.set_zlim(low - padding, high + padding)
    axis.set_xticks([0, 1], labels=["Control group", "Experiment group"])
    axis.set_yticks([])
    axis.set_zlabel("")
    axis.tick_params(axis="x", labelsize=10, pad=2)
    axis.tick_params(axis="z", labelsize=9, pad=2)
    axis.view_init(elev=23, azim=-58)
    axis.set_box_aspect((1.7, 1.0, 1.25))

    pane_color = (0.98, 0.985, 0.99, 1.0)
    axis.xaxis.set_pane_color(pane_color)
    axis.yaxis.set_pane_color(pane_color)
    axis.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    for current_axis in (axis.xaxis, axis.yaxis, axis.zaxis):
        current_axis._axinfo["grid"]["color"] = (0.78, 0.81, 0.85, 0.32)
        current_axis._axinfo["grid"]["linewidth"] = 0.55

    figure.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    return figure, axis


def save_outputs(output_dir: Path | None = None, input_path: Path | None = None,
                 seed: int = 20260709) -> dict[str, Path]:
    """Generate the chart and save raster and vector deliverables."""
    folder = output_dir if output_dir is not None else Path(__file__).resolve().parent / "output"

    data = assign_depth_positions(build_long_data(input_path), seed=seed)
    folder.mkdir(parents=True, exist_ok=True)
    figure, _ = create_figure(data)
    paths = {
        "png": folder / "paired_depth_plot.png",
        "svg": folder / "paired_depth_plot.svg",
        "pdf": folder / "paired_depth_plot.pdf",
    }
    try:
        for path in paths.values():
            figure.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    finally:
        plt.close(figure)
    return paths


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path,
                        help="Excel B/C control/experiment columns, or CSV ID,control,experiment; default: built-in values.")
    parser.add_argument("--output-dir", type=Path, help="Default: output next to this script.")
    parser.add_argument("--seed", type=int, default=20260709, help="Seed for display-only depth offsets.")
    args = parser.parse_args(argv)
    try:
        for output_type, output_path in save_outputs(args.output_dir, args.input, args.seed).items():
            print(f"{output_type.upper()}: {output_path}")
    except (OSError, ValueError, BadZipFile, pd.errors.ParserError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
