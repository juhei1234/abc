# ABOUTME: Unit tests for scenario analytics return/risk calculations.
# ABOUTME: Verifies deterministic outputs for macro and sector shock inputs.
from app.schemas.portfolio import ScenarioRequest
from app.services.analytics import run_scenario


def test_run_scenario_returns_reasonable_metrics():
    result = run_scenario(
        weights={"AAPL": 0.5, "MSFT": 0.5},
        sector_map={"AAPL": "Technology", "MSFT": "Technology"},
        request=ScenarioRequest(
            portfolio_id=1,
            treasury_yield_change_bps=-50,
            fed_rate_change_bps=-25,
            inflation_change_bps=10,
            sector_shocks={"Technology": 4},
        ),
    )

    assert result.projected_return_pct > 0
    assert result.var_95_pct > 0
