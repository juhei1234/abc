# ABOUTME: FastAPI application entrypoint configuring routers and startup table creation.
# ABOUTME: Exposes health endpoint and CORS-enabled REST APIs for frontend SPA.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.market import router as market_router
from app.api.portfolio import router as portfolio_router
from app.db.session import engine
from app.models.models import Base

app = FastAPI(title="Earnings Calendar API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(market_router)
app.include_router(portfolio_router)
