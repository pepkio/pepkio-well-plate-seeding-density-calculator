# Pepkio Cell Seeding Density Calculator

Container image bundling the Cell Seeding Density Calculator CLI so pipelines and lab systems can obtain per-well seeding volumes from the Pepkio API without a local Python install.

# What It Does

The image runs `pepkio-well-plate-seeding-density-calculator`, a client for the Pepkio Cell Seeding Density Calculator REST API. From one hemocytometer count and viability reading, it returns cells per well and pipette volume (µL) for 6W, 12W, 24W, 48W, 96W, and 384W plates, with QC badges and optional time-to-confluency estimates.

Seeding calculations support tissue culture setup, high-throughput screening plates, and assay scheduling checks. Calculator logic runs on Pepkio servers; provide a network connection and API key for `run` commands.

# Features

- All six standard plate formats with manufacturer well areas
- Viability-adjusted stock concentration
- QC badges: low viability, exceeds volume, below pipette (384W &lt; 1 µL)
- Optional doubling time and assay confluency estimates
- Named manifest examples (e.g. `hek293t_standard`, `cho_384w`)
- Manifest inspection without an API key

# Quick Start

```bash
docker pull pepkio/well-plate-seeding-density-calculator:0.1.0
docker run --rm -e PEPKIO_API_KEY="your-key" pepkio/well-plate-seeding-density-calculator:0.1.0 \
  pepkio-well-plate-seeding-density-calculator run --example hek293t_standard
```

Manifest only (no API key):

```bash
docker run --rm pepkio/well-plate-seeding-density-calculator:0.1.0 \
  pepkio-well-plate-seeding-density-calculator manifest --examples
```

# Quick Example

```bash
docker run --rm -e PEPKIO_API_KEY="$PEPKIO_API_KEY" pepkio/well-plate-seeding-density-calculator:0.1.0 \
  pepkio-well-plate-seeding-density-calculator run --input-json \
  '{"cells_per_cm2":230000,"stock_concentration_cells_per_mL":2000000,"viability_pct":95,"seeding_confluency_pct":30}'
```

# Typical Use Cases

- HEK293T seeding at 30% confluency from a 2 million cells/mL stock
- Comparing seeding volumes across 96-well and 384-well formats
- Flagging 384-well transfers below 1 µL pipette minimum
- Low-viability warnings before plating
- CI or workflow runners that need a fixed client environment

# Scientific Background

Cells needed = (seeding_confluency_pct / 100) × cells_per_cm² × well_area_cm². Effective stock = stock × (viability_pct / 100). Volume (µL) = (cells_needed / effective_stock) × 1000. Time to confluency uses log₂(assay% / seeding%) × doubling_time_h when doubling time is provided.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/well-plate-seeding-density-calculator

The web UI adds cell-line presets with literature-sourced cells/cm² and doubling times, side-by-side results for all plate formats, and shareable links.

# Documentation and Resources

GitHub Repository (source and Dockerfile): https://github.com/pepkio/pepkio-well-plate-seeding-density-calculator

Web Application: https://www.pepkio.com/tools/well-plate-seeding-density-calculator

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services.
