# ABOUTME: Pydantic schemas for portfolio CRUD, holdings, and analytics outputs.
# ABOUTME: Defines typed API contracts used by frontend portfolio workflows.
from pydantic import BaseModel, Field


class HoldingIn(BaseModel):
    ticker: str
    weight: float


class PortfolioCreate(BaseModel):
    name: str
    benchmark: str = "SPY"
    holdings: list[HoldingIn] = Field(default_factory=list)


class PortfolioOut(BaseModel):
    id: int
    name: str
    benchmark: str
    holdings: list[HoldingIn]


class ScenarioRequest(BaseModel):
    portfolio_id: int
    treasury_yield_change_bps: float = 0.0
    fed_rate_change_bps: float = 0.0
    inflation_change_bps: float = 0.0
    sector_shocks: dict[str, float] = Field(default_factory=dict)


class ScenarioResponse(BaseModel):
    projected_return_pct: float
    var_95_pct: float
    sharpe_ratio: float
    benchmark_return_pct: float
