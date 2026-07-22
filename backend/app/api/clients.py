from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.schemas.dashboard import ClientDashboardOut, NiveauConso
from app.schemas.rapport import PeriodeResumeOut, RapportOut
from app.services.consommation import SEUIL_ALERTE_PCT, calculer_pourcentage, consommation
from app.services.export import construire_rapport
from app.services.periode import periode_courante, periodes_passees, trouver_periode

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(get_current_user)],
)


def _get_client_or_404(client_id: int, db: Session) -> Client:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable")
    return client


@router.get("", response_model=list[ClientOut])
def list_clients(actif: bool | None = None, db: Session = Depends(get_db)):
    query = db.query(Client)
    if actif is not None:
        query = query.filter(Client.actif == actif)
    return query.order_by(Client.nom).all()


@router.post("", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    return _get_client_or_404(client_id, db)


@router.get("/{client_id}/dashboard", response_model=ClientDashboardOut)
def get_client_dashboard(client_id: int, db: Session = Depends(get_db)):
    client = _get_client_or_404(client_id, db)
    periode_debut, periode_fin = periode_courante(client.date_debut_contrat)
    periode = (periode_debut, periode_fin)

    minutes_n1 = consommation(db, client.id, "N1", periode)
    minutes_n2 = consommation(db, client.id, "N2", periode)
    minutes_n3 = consommation(db, client.id, "N3", periode)

    pct_n1 = calculer_pourcentage(minutes_n1, client.forfait_n1_h)
    pct_n2 = calculer_pourcentage(minutes_n2, client.forfait_n2_h)

    return ClientDashboardOut(
        client_id=client.id,
        client_nom=client.nom,
        periode_debut=periode_debut,
        periode_fin=periode_fin,
        n1=NiveauConso(forfait_h=client.forfait_n1_h, consomme_minutes=minutes_n1, pourcentage=round(pct_n1, 1)),
        n2=NiveauConso(forfait_h=client.forfait_n2_h, consomme_minutes=minutes_n2, pourcentage=round(pct_n2, 1)),
        n3=NiveauConso(forfait_h=None, consomme_minutes=minutes_n3, pourcentage=None),
        alerte=pct_n1 >= SEUIL_ALERTE_PCT or pct_n2 >= SEUIL_ALERTE_PCT,
    )


@router.get("/{client_id}/periodes", response_model=list[PeriodeResumeOut])
def list_periodes_passees(client_id: int, db: Session = Depends(get_db)):
    client = _get_client_or_404(client_id, db)
    resultats = []
    for n, debut, fin in periodes_passees(client.date_debut_contrat):
        data = construire_rapport(db, client, (debut, fin))
        resultats.append(
            PeriodeResumeOut(
                periode_id=f"{debut.year:04d}-{debut.month:02d}",
                periode_debut=debut,
                periode_fin=fin,
                n1=data["n1"],
                n2=data["n2"],
                n3=data["n3"],
                heures_supp_minutes=data["heures_supp_minutes"],
            )
        )
    return resultats


@router.get("/{client_id}/periodes/{yyyy_mm}", response_model=RapportOut)
def get_periode_detail(client_id: int, yyyy_mm: str, db: Session = Depends(get_db)):
    client = _get_client_or_404(client_id, db)
    trouvee = trouver_periode(client.date_debut_contrat, yyyy_mm)
    if trouvee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Periode introuvable")
    _, debut, fin = trouvee
    data = construire_rapport(db, client, (debut, fin))
    return RapportOut(
        client_id=client.id,
        client_nom=client.nom,
        periode_debut=debut,
        periode_fin=fin,
        n1=data["n1"],
        n2=data["n2"],
        n3=data["n3"],
        heures_supp_minutes=data["heures_supp_minutes"],
        interventions=data["interventions"],
    )


@router.patch("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    client = _get_client_or_404(client_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client


@router.post("/{client_id}/archiver", response_model=ClientOut)
def archiver_client(client_id: int, db: Session = Depends(get_db)):
    client = _get_client_or_404(client_id, db)
    client.actif = False
    db.commit()
    db.refresh(client)
    return client
