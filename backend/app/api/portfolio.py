# ABOUTME: Portfolio API routes for CRUD, import/export, and scenario analytics.
# ABOUTME: Uses authenticated user context and persisted holdings in PostgreSQL.
import csv
import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.models import Holding, Portfolio, User
from app.schemas.portfolio import HoldingIn, PortfolioCreate, PortfolioOut, ScenarioRequest, ScenarioResponse
from app.services.analytics import run_scenario

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])


@router.post("", response_model=PortfolioOut)
def create_portfolio(payload: PortfolioCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = Portfolio(name=payload.name, benchmark=payload.benchmark, user_id=user.id)
    db.add(portfolio)
    db.flush()
    for row in payload.holdings:
        db.add(Holding(portfolio_id=portfolio.id, ticker=row.ticker.upper(), weight=row.weight))
    db.commit()
    db.refresh(portfolio)
    return PortfolioOut(
        id=portfolio.id,
        name=portfolio.name,
        benchmark=portfolio.benchmark,
        holdings=[HoldingIn(ticker=h.ticker, weight=h.weight) for h in portfolio.holdings],
    )


@router.get("", response_model=list[PortfolioOut])
def list_portfolios(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Portfolio).filter(Portfolio.user_id == user.id).all()
    return [
        PortfolioOut(
            id=row.id,
            name=row.name,
            benchmark=row.benchmark,
            holdings=[HoldingIn(ticker=h.ticker, weight=h.weight) for h in row.holdings],
        )
        for row in rows
    ]


@router.post("/import/{portfolio_id}")
def import_holdings(portfolio_id: int, file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id, Portfolio.user_id == user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    db.query(Holding).filter(Holding.portfolio_id == portfolio.id).delete()
    for row in reader:
        db.add(Holding(portfolio_id=portfolio.id, ticker=row["ticker"].upper(), weight=float(row["weight"])))
    db.commit()
    return {"status": "ok"}


@router.get("/export/{portfolio_id}")
def export_holdings(portfolio_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id, Portfolio.user_id == user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ticker", "weight"])
    for holding in portfolio.holdings:
        writer.writerow([holding.ticker, holding.weight])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv")


@router.post("/scenario", response_model=ScenarioResponse)
def scenario_analysis(payload: ScenarioRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == payload.portfolio_id, Portfolio.user_id == user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    weights = {holding.ticker: holding.weight for holding in portfolio.holdings}
    sector_map = {ticker: "Technology" for ticker in weights}
    return run_scenario(weights, sector_map, payload)
