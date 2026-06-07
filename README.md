# Pepkio Cell Seeding Density Calculator

Python client for the Pepkio Cell Seeding Density Calculator: compute cells per well and pipette volume across six standard plate formats from one hemocytometer count and a target seeding confluency.

# Overview

Cell culture experiments often require seeding adherent cells at a defined density so that wells reach a target confluency by assay day. Researchers typically count cells with a hemocytometer or automated counter, apply a trypan blue viability correction, and then calculate how many live cells to add per well. The arithmetic depends on well surface area, which differs across 6-, 12-, 24-, 48-, 96-, and 384-well plates. A single hemocytometer reading must be converted separately for each format, and viability must be applied to the stock concentration before volume is computed.

Manual spreadsheet calculations are error-prone when switching between plate formats, when viability is low, or when 384-well transfers fall below practical pipette limits. Confluency targets (for example 20–30% at seeding versus 70–80% at assay) and population doubling time add further steps when estimating whether cultures will be ready on schedule.

The [Pepkio Cell Seeding Density Calculator](https://www.pepkio.com/tools/well-plate-seeding-density-calculator) web application computes cells per well and pipette volume (µL) for all six standard plate formats from one stock count and seeding confluency target. This repository provides the **Python client** (`pepkio-well-plate-seeding-density-calculator`) that calls the same calculation engine through the Pepkio Tools REST API, so you can generate seeding plans from scripts, Jupyter notebooks, or automated pipelines.

If you prefer a graphical interface, use the hosted tool at [https://www.pepkio.com/tools/well-plate-seeding-density-calculator](https://www.pepkio.com/tools/well-plate-seeding-density-calculator). If you need reproducible, programmatic access, install the package from [PyPI](https://pypi.org/project/pepkio-well-plate-seeding-density-calculator/) and follow the Quick Start below.

# Features

## Seeding calculations (API-backed)

- **All six plate formats:** 6W, 12W, 24W, 48W, 96W, and 384W with manufacturer well areas (Corning/Falcon specifications)
- **Viability adjustment:** effective stock concentration = hemocytometer count × (viability % / 100)
- **Cells per well:** from target seeding confluency %, cells per cm² at 100% confluency, and well area
- **Pipette volume (µL):** volume of cell suspension to add per well
- **QC badges per plate:** `ok`, `low_viability` (viability &lt; 70%), `exceeds_volume` (above recommended working volume), `below_pipette` (384W volume &lt; 1 µL)
- **Time to confluency:** estimate hours to reach assay confluency from population doubling time (optional)
- **Assay scheduling:** optional assay datetime to compare estimated growth time against a deadline
- **Validation warnings:** stock concentration range, viability minimum, doubling time range, contact-inhibition note near confluency
- **Shareable runs:** API runs return `permalink` and `result_url` fields when available

## Python package

- Fetch the tool manifest and list named examples (`get_manifest`, `list_examples`, `get_example_input`)
- Run calculations synchronously (`run`) with custom JSON or manifest examples
- Poll runs for async tools (`get_run`, `wait_for_run`)
- CLI for manifest inspection and one-off runs (`pepkio-well-plate-seeding-density-calculator`)
- Configurable API base URL and API keys via environment variables

# Common Use Cases

### HEK293T seeding at 30% confluency (`hek293t_standard`)

Seed HEK293T from a 2 million cells/mL stock at 95% viability with a 30% seeding confluency target. The planner returns volumes for all six plate formats and estimates ~38 hours to reach 80% confluency with a 27-hour doubling time.

### HeLa seeding at 25% confluency (`hela_seeding`)

Plan HeLa seeding from 1.8 million cells/mL at 98% viability with a 25% seeding target and 70% assay confluency goal, using literature-based cells/cm² and doubling time inputs.

### Low viability warning (`low_viability_warn`)

Count shows 65% viability after trypan blue. The calculator applies viability to stock concentration and flags `low_viability` on plate rows where viability is below 70%.

### 384-well sub-microliter transfer (`cho_384w`)

CHO-K1 seeding at 20% confluency from a 3 million cells/mL stock may produce a 384-well transfer below 1 µL, triggering a `below_pipette` badge that signals impractical pipetting on standard P2/P10 pipettes.

### Invalid stock concentration (`invalid_stock`)

Stock counts outside 1×10³–1×10⁸ cells/mL return blocking errors and prevent volume calculation until inputs are corrected.

# Why This Tool Exists

Spreadsheets and single-plate calculators require recalculating cells per well and suspension volume whenever you switch from a 96-well to a 384-well layout or compare multiple formats side by side. Viability correction is easy to omit when dividing by total counted cells rather than live cells only.

384-well seeding often produces transfer volumes below 1 µL, which standard air-displacement pipettes cannot deliver reliably without diluting the stock or adjusting seeding density. Manual checks against manufacturer maximum working volumes per well are rarely built into ad hoc spreadsheets.

The Pepkio Cell Seeding Density Calculator computes all six plate formats from one hemocytometer reading, applies viability to stock concentration, flags low viability and impractical volumes, and optionally estimates time to assay confluency from doubling time. The Python package in this repository calls the same API for scripted or automated workflows.

# Installation

Install from PyPI:

```bash
pip install pepkio-well-plate-seeding-density-calculator
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add pepkio-well-plate-seeding-density-calculator
```

PyPI package: [https://pypi.org/project/pepkio-well-plate-seeding-density-calculator/](https://pypi.org/project/pepkio-well-plate-seeding-density-calculator/)

## API key

Programmatic runs require a Pepkio API key with **tools:run** scope. Create one at [https://www.pepkio.com/account/api-keys](https://www.pepkio.com/account/api-keys).

```bash
export PEPKIO_API_KEY="your-key"
```

| Variable | Description |
|----------|-------------|
| `PEPKIO_API_KEY` | Production (or default) API key |
| `LOCAL_PEPKIO_API_KEY` | Local dev key when base URL points to `tools.localtest.me` |
| `PEPKIO_API_BASE_URL` | Override API host (default: `https://tools.pepkio.com`) |
| `PEPKIO_SSL_VERIFY` | Set to `0` or `false` to disable TLS verify (local dev disables verify for `localtest.me` by default) |

Local development against a staging stack:

```bash
export PEPKIO_API_BASE_URL=https://tools.localtest.me
export PEPKIO_API_KEY="$LOCAL_PEPKIO_API_KEY"
```

Web UI (local): [https://www.localtest.me/tools/well-plate-seeding-density-calculator](https://www.localtest.me/tools/well-plate-seeding-density-calculator)

# Quick Start

Manifest inspection does **not** require an API key. Running the tool does.

### Python: manifest example

```python
from pepkio_well_plate_seeding_density_calculator import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("hek293t_standard")
    result = client.run(inp)
    print(result.status, result.permalink)
    for plate in result.result.get("plates", []):
        print(plate["format"], plate["cells_per_well"], plate["volume_uL"], plate["badges"])
    ttc = result.result.get("time_to_confluency")
    if ttc:
        print("Hours to confluency:", ttc.get("hours"))
```

### Python: custom input

```python
from pepkio_well_plate_seeding_density_calculator import PepkioClient

inp = {
    "cells_per_cm2": 230000,
    "stock_concentration_cells_per_mL": 2000000,
    "viability_pct": 95,
    "seeding_confluency_pct": 30,
    "doubling_time_h": 27,
    "assay_confluency_pct": 80,
}

with PepkioClient() as client:
    result = client.run(inp)
    assert result.status == "completed"
```

### CLI

```bash
# Manifest (no API key)
pepkio-well-plate-seeding-density-calculator manifest
pepkio-well-plate-seeding-density-calculator manifest --examples

# Run a named example (API key required)
pepkio-well-plate-seeding-density-calculator run --example hek293t_standard

# Run custom JSON input
pepkio-well-plate-seeding-density-calculator run --input-json '{
  "cells_per_cm2": 230000,
  "stock_concentration_cells_per_mL": 2000000,
  "viability_pct": 95,
  "seeding_confluency_pct": 30
}'
```

Options: `--api-key`, `--base-url`, `--label`, `--idempotency-key`.

# Example Output

A completed run for the `hek293t_standard` manifest example (HEK293T, 2 million cells/mL, 95% viability, 30% seeding confluency, 27 h doubling time, 80% assay confluency target) returns a structure similar to:

```json
{
  "run_id": "…",
  "status": "completed",
  "permalink": "https://tools.pepkio.com/r/…",
  "result": {
    "has_blocking_errors": false,
    "time_to_confluency": {
      "hours": 38,
      "assay_confluency_pct": 80
    },
    "plates": [
      {
        "format": "96W",
        "well_area_cm2": 0.32,
        "cells_per_well": 22080,
        "volume_uL": 11.62,
        "badges": ["ok"]
      }
    ],
    "warnings": []
  }
}
```

The full response includes rows for all six plate formats (6W through 384W). The `permalink` field links to a saved run that colleagues can open to review the same parameters and results.

# Scientific Background

## Seeding density and confluency

**Seeding density** is the number of cells plated per unit area (cells/cm²) or per well. **Confluency** describes what fraction of the well surface is covered by cells at a given time. Researchers often seed at a fraction of confluency (for example 20–40%) so cells have room to proliferate before an assay.

**Cells per cm² at 100% confluency** is a cell-line-specific reference density representing a fully confluent monolayer. Multiplying by well surface area and the seeding confluency fraction gives cells needed per well:

**cells_needed = (seeding_confluency_pct / 100) × cells_per_cm² × well_area_cm²**

## Viability correction

Hemocytometer counts include dead and live cells unless corrected. Trypan blue viability reports the percentage of live cells. Only live cells contribute to effective stock concentration:

**effective_stock = stock_concentration_cells_per_mL × (viability_pct / 100)**

## Pipette volume

The volume of cell suspension to transfer into each well (µL) is:

**volume_uL = (cells_needed / effective_stock) × 1000**

## Well surface areas

Well areas used in calculations follow Corning/Falcon manufacturer specifications:

| Format | Well area (cm²) | Max working volume (µL) |
|--------|-----------------|-------------------------|
| 6W | 9.5 | 2900 |
| 12W | 3.8 | 1140 |
| 24W | 1.9 | 570 |
| 48W | 0.95 | 285 |
| 96W | 0.32 | 200 |
| 384W | 0.1 | 110 |

## Time to assay confluency

When population doubling time is provided, the tool estimates hours to reach the assay confluency target assuming exponential growth:

**doublings = log₂(assay_confluency_pct / seeding_confluency_pct)**

**hours = doublings × doubling_time_h**

If an assay datetime is supplied, the result can include whether the culture is expected to reach target confluency before that deadline. A warning notes that contact inhibition near confluency may slow growth above roughly 70% confluency.

## QC badges

- **low_viability:** viability below 70% may reduce reproducibility
- **exceeds_volume:** calculated volume exceeds the recommended working volume for that plate format
- **below_pipette:** 384-well volume below 1 µL is impractical for standard pipettes
- **ok:** no QC issues flagged for that plate row

# Frequently Asked Questions

### What is cell seeding density?

Cell seeding density is the number of cells added per well or per cm² when plating a culture. It determines how quickly cells reach confluency and affects assay timing, morphology, and experimental reproducibility.

### How do I calculate cells per well for a 96-well plate?

Multiply the target seeding confluency fraction by cells per cm² at 100% confluency, then multiply by the 96-well surface area (0.32 cm² for standard Corning/Falcon plates). The [Pepkio Cell Seeding Density Calculator](https://www.pepkio.com/tools/well-plate-seeding-density-calculator) performs this for all six standard formats from one stock count.

### What confluency should I seed at?

Common seeding confluencies are 20–40% for adherent lines that will be assayed in 1–3 days, but optimal values depend on cell line, doubling time, and assay requirements. The tool accepts seeding confluency between 10% and 100% with a warning outside typical ranges.

### How does trypan blue viability affect seeding volume?

Viability percentage scales the hemocytometer stock concentration to live cells only. If you count 2×10⁶ cells/mL with 90% viability, effective stock is 1.8×10⁶ live cells/mL. Omitting viability over-seeds wells and wastes cells, or under-seeds if dead cells are included in the count.

### What is cells per cm² at 100% confluency?

It is the cell density of a fully confluent monolayer for a given line, usually measured or taken from vendor literature (ATCC, DSMZ, Gibco reference values). The web application includes presets for common lines such as HEK293T, HeLa, CHO-K1, and NIH/3T3 with literature-sourced values.

### How do I convert hemocytometer count to volume per well?

Divide cells needed per well by the viability-adjusted stock concentration (cells/mL), then multiply by 1000 to convert mL to µL. The formula is volume_uL = (cells_needed / effective_stock) × 1000.

### Why is my 384-well volume flagged below pipette?

384-well plates have small surface area (0.1 cm²). At moderate seeding densities, required volume can fall below 1 µL, which is below the reliable range of standard P2 pipettes. Dilute the stock or increase seeding density to obtain a pipettable volume.

### What does the exceeds_volume badge mean?

The calculated transfer volume exceeds the recommended maximum working volume for that plate format (for example 200 µL for 96-well or 110 µL for 384-well). Reduce seeding density, use a more concentrated stock, or choose a larger well format.

### How do I estimate when cells will reach 80% confluency?

Provide population doubling time and optional assay confluency target. The tool computes doublings = log₂(assay% / seeding%) and multiplies by doubling time. Example: seeding at 30% toward 80% confluency requires log₂(80/30) ≈ 1.42 doublings; at 27 h doubling time, that is ~38 hours.

### What stock concentration range is accepted?

Stock concentration must be between 1×10³ and 1×10⁸ cells/mL. Values outside this range return blocking errors.

### What is the minimum acceptable viability?

Viability must be at least 50%. Below 50% is a blocking error. Between 50% and 70%, calculation proceeds but plates receive a `low_viability` warning.

### Can I use this for suspension cell lines?

The web application includes presets for suspension lines (Jurkat, K562) with a note that cells/cm² is not the standard metric for suspension culture. Adherent seeding formulas apply to monolayer plating; interpret suspension presets with caution.

### Do I need an API key for the Python client?

No key is required for `get_manifest()` or the CLI `manifest` command. `run()` and the CLI `run` command require an API key with tools:run scope.

### Can I run the tool offline?

The Python package calls the hosted Pepkio Tools API; an internet connection and valid API key are required for runs. Seeding calculations are not bundled for fully offline use in this package.

### How do I share a seeding plan with a colleague?

Share the `permalink` returned from an API run, or use the shareable link feature in the [web application](https://www.pepkio.com/tools/well-plate-seeding-density-calculator). The link restores the same stock count, viability, confluency targets, and plate results.

### What is the difference between seeding confluency and assay confluency?

Seeding confluency is the target coverage at the time of plating (for example 30%). Assay confluency is the coverage goal for the experiment (for example 70–80%). Doubling time estimates use both values to predict hours until the assay target is reached.

### Which plate formats are supported?

6-well (6W), 12-well (12W), 24-well (24W), 48-well (48W), 96-well (96W), and 384-well (384W) with well areas from Corning/Falcon manufacturer specifications.

### How do I seed HEK293T in a 96-well plate from 2 million cells/mL?

Enter cells per cm² (for example 230000 for HEK293T), stock 2000000 cells/mL, viability, and seeding confluency (for example 30%). The `hek293t_standard` manifest example illustrates this workflow and returns 22,080 cells per 96-well with 11.62 µL transfer at 95% viability.

# Web Application

For interactive planning without writing code, use the hosted Pepkio Cell Seeding Density Calculator.

The web interface accepts hemocytometer stock concentration, trypan blue viability, cells per cm² at 100% confluency, seeding and assay confluency targets, and optional population doubling time. It returns a table of cells per well and pipette volume for all six plate formats with QC badges for low viability, excessive volume, and sub-microliter 384-well transfers.

The web UI also supports:

- **Cell line presets** — approximately 30 common lines (HeLa, HEK293, HEK293T, CHO-K1, NIH/3T3, and others) with literature-sourced cells/cm² and doubling time values
- **Time-to-confluency estimate** — hours to reach assay confluency from doubling time, with optional assay deadline check
- **Interactive results table** — side-by-side comparison across 6W, 12W, 24W, 48W, 96W, and 384W formats
- **Shareable link** — restores the exact parameters and results for collaborators

**Web Application:** [https://www.pepkio.com/tools/well-plate-seeding-density-calculator](https://www.pepkio.com/tools/well-plate-seeding-density-calculator)

# Related Resources

- **GitHub Repository:** [https://github.com/pepkio/pepkio-well-plate-seeding-density-calculator](https://github.com/pepkio/pepkio-well-plate-seeding-density-calculator)
- **PyPI Package:** [https://pypi.org/project/pepkio-well-plate-seeding-density-calculator/](https://pypi.org/project/pepkio-well-plate-seeding-density-calculator/)
- **Web Application:** [https://www.pepkio.com/tools/well-plate-seeding-density-calculator](https://www.pepkio.com/tools/well-plate-seeding-density-calculator)

# About Pepkio

[Pepkio](https://www.pepkio.com) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (RNA-seq, single-cell RNA-seq, spatial transcriptomics, functional enrichment, and custom workflows).

# Keywords

cell seeding density, seeding density calculator, cells per well calculator, well plate seeding, tissue culture seeding, cell culture calculator, hemocytometer calculator, trypan blue viability, seeding confluency, confluency calculator, cells per cm2, cell plating density, 96-well seeding, 384-well seeding, 6-well plate seeding, 24-well plate seeding, microplate seeding, adherent cell seeding, HEK293T seeding density, HeLa seeding density, CHO cell seeding, NIH 3T3 seeding, population doubling time, time to confluency, assay confluency, cell suspension volume, pipette volume calculator, microliter cell seeding, viability correction cell count, live cell concentration, stock cells per mL, cell culture planning, laboratory cell calculator, Pepkio, pepkio-well-plate-seeding-density-calculator, Python cell seeding API, lab automation cell culture, multi-plate format seeding, Corning well area, Falcon plate area, QC badge seeding, low viability warning, below pipette 384 well, exceeds volume warning, cell line preset seeding, exponential growth estimate, contact inhibition confluency, molecular biology calculator, bench cell seeding protocol

how to calculate cells per well for 96 well plate, how many cells to seed per well from hemocytometer count, cell seeding density calculator with viability correction, trypan blue viability seeding volume formula, how to seed HEK293T at 30 percent confluency, calculate microliter volume for cell seeding 96 well, 384 well plate seeding volume below 1 uL, compare seeding volumes across 6 12 24 48 96 384 well plates, what is cells per cm2 at 100 percent confluency, how to estimate time to 80 percent confluency from doubling time, seeding confluency versus assay confluency explained, when will HeLa reach 70 percent confluency after seeding at 25 percent, how to correct hemocytometer count for viability, minimum viability for cell seeding calculation, stock concentration cells per mL valid range, how to plan cell seeding for high throughput 384 well screen, CHO-K1 seeding density 384 well plate, low viability cell seeding warning tissue culture, effective live cell concentration from trypan blue, log2 doublings time to confluency formula, shareable cell seeding plan link Pepkio, Python script cell seeding density all plate formats, API for well plate seeding calculator, automate cell seeding worksheet from notebook, cell line preset HEK293T cells per cm2 doubling time, suspension cell line Jurkat seeding caveat, contact inhibition slows growth above 70 percent confluency warning, manufacturer well area Corning Falcon seeding math, how many live cells per well at 30 percent seeding, plan tissue culture seeding from one hemocytometer reading, Pepkio cell seeding density calculator web tool, seeding density for drug screening 96 well assay, reproducible cell plating across plate formats

# Contributing

Clone [https://github.com/pepkio/pepkio-well-plate-seeding-density-calculator](https://github.com/pepkio/pepkio-well-plate-seeding-density-calculator), run `uv sync`, and execute `uv run pytest` for unit and integration tests. Integration tests require `PEPKIO_API_KEY` or `LOCAL_PEPKIO_API_KEY` in the environment.
