# SPDX-License-Identifier: MIT
"""Typed API request/response models (from manifest input/output schemas)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .exceptions import PepkioAPIError


class RunOptions(BaseModel):
    """Optional fields for POST .../run."""

    idempotency_key: str | None = None
    label: str | None = None


class WellPlateSeedingDensityToolInput(BaseModel):
    """Tool input (manifest: cells_per_cm2, stock, viability, seeding confluency required)."""

    model_config = ConfigDict(extra="allow")

    cells_per_cm2: float = Field(..., description="Cells per cm² at 100% confluency")
    stock_concentration_cells_per_mL: float
    viability_pct: float = Field(..., description="Trypan blue viability (live cells only)")
    seeding_confluency_pct: float = Field(..., description="Target confluency at seeding (10–100%)")
    cell_line_name: str | None = None
    doubling_time_h: float | None = Field(
        default=None, description="Population doubling time in hours"
    )
    assay_confluency_pct: float | None = Field(
        default=None, description="Confluency goal for assay timing (default 80%)"
    )
    assay_datetime: str | None = Field(
        default=None, description="Optional ISO datetime for assay scheduling"
    )


class WellPlateSeedingDensityToolOutput(BaseModel):
    """Tool handler output shape (from manifest output schema)."""

    model_config = ConfigDict(extra="allow")

    plates: list[Any] | None = None
    time_to_confluency: dict[str, Any] | None = None
    warnings: list[Any] | None = None
    has_blocking_errors: bool | None = None


class RunResult(BaseModel):
    """Tool run response envelope."""

    model_config = ConfigDict(extra="allow")

    run_id: str
    status: str
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    result_url: str | None = None
    permalink: str | None = None
    duration_ms: int | None = None

    def raise_for_error(self) -> None:
        """Raise PepkioAPIError if the run response includes an error field."""
        if self.error is None:
            return
        err = self.error
        raise PepkioAPIError(
            err.get("message", "Tool run failed"),
            code=err.get("code"),
            details=err.get("details") if isinstance(err.get("details"), dict) else {},
            response_body={"run_id": self.run_id, "status": self.status, "error": self.error},
        )


def parse_run_response(data: dict[str, Any]) -> RunResult:
    """Parse a run API JSON body into RunResult."""
    return RunResult.model_validate(data)
