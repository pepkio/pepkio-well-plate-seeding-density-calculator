"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest

from pepkio_well_plate_seeding_density_calculator.client import PepkioClient
from pepkio_well_plate_seeding_density_calculator.exceptions import PepkioAPIError

ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]

EXPECTED_EXAMPLES = (
    "hek293t_standard",
    "hela_seeding",
    "low_viability_warn",
    "invalid_stock",
    "cho_384w",
)


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


def _resolve_environments() -> list[tuple[str, str]]:
    override = os.getenv("PEPKIO_API_BASE_URL")
    if override:
        name = "local" if "localtest.me" in override else "production"
        return [(name, override.rstrip("/"))]
    return ENVIRONMENTS


@pytest.fixture(params=_resolve_environments(), ids=lambda p: p[0])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        try:
            client.get_manifest(refresh=True)
        except PepkioAPIError as exc:
            if exc.status_code == 404 and exc.code == "TOOL_NOT_FOUND":
                pytest.skip(f"Tool not deployed on {env_name} ({base_url})")
            raise
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "well-plate-seeding-density-calculator"
    names = live_client.list_examples()
    for expected in EXPECTED_EXAMPLES:
        assert expected in names


def test_run_hek293t_standard(live_client: PepkioClient):
    inp = live_client.get_example_input("hek293t_standard")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is False
    vessels = result.result.get("vessels")
    assert isinstance(vessels, list)
    assert len(vessels) >= 1
    plate_96w = next((p for p in vessels if p.get("format") == "96W"), None)
    assert plate_96w is not None
    assert plate_96w.get("cells_per_vessel") is not None
    assert plate_96w.get("volume_uL") is not None


def test_run_hela_seeding(live_client: PepkioClient):
    inp = live_client.get_example_input("hela_seeding")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is False


def test_run_cho_384w(live_client: PepkioClient):
    inp = live_client.get_example_input("cho_384w")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is False
    vessels = result.result.get("vessels")
    assert isinstance(vessels, list)
    plate_384w = next((p for p in vessels if p.get("format") == "384W"), None)
    assert plate_384w is not None
    badges = plate_384w.get("badges") or []
    assert "below_pipette" in badges


def test_run_invalid_stock(live_client: PepkioClient):
    inp = live_client.get_example_input("invalid_stock")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is True
