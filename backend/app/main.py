import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.auth import router as auth_router
from app.api.clients import router as clients_router
from app.api.interventions import router as interventions_router
from app.api.rapports import router as rapports_router
from app.api.alertes import router as alertes_router
from app.config import settings
from app.core.limiter import limiter
from app.core.security import hash_password
from app.database import SessionLocal
from app.models.user import User

logger = logging.getLogger(__name__)

# Doc interactive fermée en production : le port du backend peut être joignable
# directement (hors du proxy frontend), donc /docs et /openapi.json seraient
# sinon accessibles à quiconque atteint ce port.
_docs = {"docs_url": None, "redoc_url": None, "openapi_url": None} if settings.environment == "production" else {}

app = FastAPI(title="ForfaitFlow API", version="0.1.0", **_docs)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(clients_router, prefix="/api/v1")
app.include_router(interventions_router, prefix="/api/v1")
app.include_router(rapports_router, prefix="/api/v1")
app.include_router(alertes_router, prefix="/api/v1")


@app.on_event("startup")
def seed_admin_user() -> None:
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == settings.admin_email).first()
        if existing is None:
            db.add(
                User(
                    email=settings.admin_email,
                    hash_password=hash_password(settings.admin_password),
                    nom_affichage="Mickaël Tavenart",
                    role="admin",
                )
            )
            db.commit()
    except Exception:
        logger.warning("Seed admin ignoré (migrations non appliquées ?)")
    finally:
        db.close()


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
