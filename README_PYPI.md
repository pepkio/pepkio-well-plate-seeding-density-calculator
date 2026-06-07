# Pepkio Cell Seeding Density Calculator

Call the Pepkio cell-seeding engine from Python to obtain per-well cell counts and suspension volumes for six standard plate formats, with viability-adjusted stock concentration and QC flags for impractical transfers.

# What It Does

After a hemocytometer count, bench work often means recalculating cells per well and microliter transfer volume for each plate format you might use. Viability correction and 384-well sub-microliter volumes are easy to miss in a spreadsheet.

This package calls the same Pepkio Tools calculation engine as the hosted web application. Supply cells per cm² at confluency, stock concentration, trypan blue viability, and target seeding confluency; receive cells per well and pipette volume for 6W through 384W, optional time-to-confluency estimates, and QC badges.

Programmatic runs require a network connection and a Pepkio API key. Calculations are not bundled for offline use.

# Features

- All six standard formats: 6W, 12W, 24W, 48W, 96W, 384W
- Viability-adjusted effective stock concentration
- QC badges: low viability, exceeds volume, below pipette (384W &lt; 1 µL)
- Optional doubling time and assay confluency for growth estimates
- Manifest and named examples: `get_manifest`, `list_examples`, `get_example_input`
- CLI: `pepkio-well-plate-seeding-density-calculator manifest` and `run`
- Configuration via `PEPKIO_API_KEY` and `PEPKIO_API_BASE_URL`

# Installation

```bash
pip install pepkio-well-plate-seeding-density-calculator
```

Set an API key with **tools:run** scope before calling `run()`:

```bash
export PEPKIO_API_KEY="your-key"
```

Create a key in your [Pepkio account API keys](https://www.pepkio.com/account/api-keys) settings.

# Quick Example

```python
from pepkio_well_plate_seeding_density_calculator import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("hek293t_standard")
    result = client.run(inp)
    for plate in result.result.get("plates", []):
        print(plate["format"], plate["cells_per_well"], plate["volume_uL"], plate["badges"])
```

CLI:

```bash
pepkio-well-plate-seeding-density-calculator run --example hek293t_standard
```

Manifest inspection does not require an API key.

# Typical Use Cases

- HEK293T seeding at 30% confluency from a 2 million cells/mL stock
- HeLa plating with literature-based cells/cm² and doubling time
- Checking 384-well transfers for sub-microliter pipetting limits
- Flagging low viability (&lt; 70%) before plating
- Estimating hours to reach 80% confluency for assay scheduling
- Automating seeding worksheets in LIMS or notebook pipelines

# Scientific Background

Cells needed per well = (seeding_confluency_pct / 100) × cells_per_cm² × well_area_cm². Effective stock = stock_concentration_cells_per_mL × (viability_pct / 100). Volume (µL) = (cells_needed / effective_stock) × 1000.

Well areas follow Corning/Falcon specifications (96W: 0.32 cm²; 384W: 0.1 cm²). When doubling time is provided, hours to assay confluency = log₂(assay% / seeding%) × doubling_time_h.

# Web Application

For researchers who prefer a graphical interface, an interactive [Cell Seeding Density Calculator](https://www.pepkio.com/tools/well-plate-seeding-density-calculator) is available in the browser.

The web interface adds cell-line presets with literature-sourced cells/cm² and doubling times, side-by-side results for all plate formats, and shareable links that restore the same plan as API `permalink` values.

# Documentation and Resources

Source code and issue tracking: [github.com/pepkio/pepkio-well-plate-seeding-density-calculator](https://github.com/pepkio/pepkio-well-plate-seeding-density-calculator)

Web application: [https://www.pepkio.com/tools/well-plate-seeding-density-calculator](https://www.pepkio.com/tools/well-plate-seeding-density-calculator)

# About Pepkio

Pepkio develops software tools and provides bioinformatics analysis services for life science research. See https://www.pepkio.com for additional tools and services.

# Keywords

cell seeding density, cells per well, well plate seeding, hemocytometer viability, seeding confluency, 96-well seeding, 384-well seeding, tissue culture calculator, trypan blue correction, pipette volume seeding, time to confluency, population doubling time, HEK293T seeding, HeLa seeding, CHO seeding, multi-plate seeding, QC badge seeding, low viability warning, below pipette 384 well, Pepkio, pepkio-well-plate-seeding-density-calculator, Python cell culture API, lab automation seeding, how to calculate cells per well from hemocytometer count, viability adjusted stock concentration formula, seeding volume for 96 well plate from cells per mL, check 384 well seeding below 1 microliter, estimate hours to 80 percent confluency doubling time, compare seeding across 6 12 24 48 96 384 well formats, automate cell seeding plan from Python script, API for tissue culture seeding calculator, HEK293T 30 percent seeding 2 million per mL example, shareable cell seeding protocol link, cell line preset cells per cm2 web calculator
