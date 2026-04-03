# ABOUTME: Scenario and risk analytics helpers for portfolio simulation outcomes.
# ABOUTME: Computes projected return, VaR, and Sharpe-like metrics from shocks.
import math

from app.schemas.portfolio import ScenarioRequest, ScenarioResponse


def run_scenario(weights: dict[str, float], sector_map: dict[str, str], request: ScenarioRequest) -> ScenarioResponse:
    macro_alpha = (
        -0.02 * (request.treasury_yield_change_bps / 100)
        - 0.015 * (request.fed_rate_change_bps / 100)
        - 0.01 * (request.inflation_change_bps / 100)
    )

    shock_effect = 0.0
    for ticker, weight in weights.items():
        sector = sector_map.get(ticker, "Other")
        shock_effect += weight * (request.sector_shocks.get(sector, 0.0) / 100)

    projected_return = (macro_alpha + shock_effect) * 100
    volatility = max(4.0, 12.0 + abs(request.fed_rate_change_bps) * 0.01)
    var_95 = 1.65 * volatility
    sharpe = projected_return / volatility if volatility else 0.0
    benchmark = projected_return * 0.85 - math.copysign(0.8, projected_return or 1)

    return ScenarioResponse(
        projected_return_pct=round(projected_return, 2),
        var_95_pct=round(var_95, 2),
        sharpe_ratio=round(sharpe, 2),
        benchmark_return_pct=round(benchmark, 2),
    )
