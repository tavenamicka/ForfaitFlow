from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.schemas.alerte import AlerteOut
from app.services.consommation import alertes_actives

router = APIRouter(prefix="/alertes", tags=["alertes"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[AlerteOut])
def list_alertes(db: Session = Depends(get_db)):
    alertes = alertes_actives(db)
    return sorted(alertes, key=lambda a: a["pourcentage"], reverse=True)
