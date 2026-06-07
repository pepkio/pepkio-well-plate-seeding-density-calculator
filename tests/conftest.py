"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env, override=True)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env, override=True)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "well-plate-seeding-density-calculator",
        "title": "Cell Seeding Density Calculator",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "hek293t_standard",
                "input": {
                    "cell_line_name": "HEK293T",
                    "cells_per_cm2": 230000,
                    "doubling_time_h": 27,
                    "stock_concentration_cells_per_mL": 2000000,
                    "viability_pct": 95,
                    "seeding_confluency_pct": 30,
                    "assay_confluency_pct": 80,
                },
                "output": {
                    "has_blocking_errors": False,
                    "time_to_confluency": {"hours": 38, "assay_confluency_pct": 80},
                    "plates": [
                        {
                            "format": "96W",
                            "cells_per_well": 22080,
                            "volume_uL": 11.62,
                            "badges": ["ok"],
                        }
                    ],
                },
            },
            {
                "name": "hela_seeding",
                "input": {
                    "cell_line_name": "HeLa",
                    "cells_per_cm2": 125000,
                    "doubling_time_h": 24,
                    "stock_concentration_cells_per_mL": 1800000,
                    "viability_pct": 98,
                    "seeding_confluency_pct": 25,
                    "assay_confluency_pct": 70,
                },
                "output": {"has_blocking_errors": False},
            },
            {
                "name": "low_viability_warn",
                "input": {
                    "cells_per_cm2": 200000,
                    "doubling_time_h": 24,
                    "stock_concentration_cells_per_mL": 1500000,
                    "viability_pct": 65,
                    "seeding_confluency_pct": 30,
                    "assay_confluency_pct": 80,
                },
                "output": {"has_blocking_errors": False},
            },
            {
                "name": "invalid_stock",
                "input": {
                    "cells_per_cm2": 200000,
                    "stock_concentration_cells_per_mL": 100,
                    "viability_pct": 95,
                    "seeding_confluency_pct": 30,
                },
                "output": {"has_blocking_errors": True},
            },
            {
                "name": "cho_384w",
                "input": {
                    "cell_line_name": "CHO-K1",
                    "cells_per_cm2": 100000,
                    "doubling_time_h": 18,
                    "stock_concentration_cells_per_mL": 3000000,
                    "viability_pct": 97,
                    "seeding_confluency_pct": 20,
                    "assay_confluency_pct": 80,
                },
                "output": {
                    "has_blocking_errors": False,
                    "plates": [
                        {
                            "format": "384W",
                            "cells_per_well": 2000,
                            "volume_uL": 0.69,
                            "badges": ["below_pipette"],
                        }
                    ],
                },
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "has_blocking_errors": False,
            "time_to_confluency": {"hours": 38, "assay_confluency_pct": 80},
            "plates": [
                {
                    "format": "96W",
                    "cells_per_well": 22080,
                    "volume_uL": 11.62,
                    "badges": ["ok"],
                },
                {
                    "format": "24W",
                    "cells_per_well": 110400,
                    "volume_uL": 58.11,
                    "badges": ["ok"],
                },
            ],
            "warnings": [],
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
