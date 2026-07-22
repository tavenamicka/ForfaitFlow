from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.client import Client
from app.schemas.rapport import RapportOut
from app.services.export import construire_rapport, generer_excel, generer_pdf, nom_fichier_sur
from app.services.periode import periode_courante, trouver_periode

router = APIRouter(prefix="/rapports", tags=["rapports"], dependencies=[Depends(get_current_user)])


def _get_client_et_rapport(client_id: int, periode: str, db: Session) -> dict:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable")

    if periode == "courante":
        periode_dates = periode_courante(client.date_debut_contrat)
    else:
        trouvee = trouver_periode(client.date_debut_contrat, periode)
        if trouvee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Periode introuvable (attendu 'courante' ou 'yyyy-mm')",
            )
        _, debut, fin = trouvee
        periode_dates = (debut, fin)

    return construire_rapport(db, client, periode_dates)


@router.get("/{client_id}", response_model=RapportOut)
def get_rapport(client_id: int, periode: str = "courante", db: Session = Depends(get_db)):
    data = _get_client_et_rapport(client_id, periode, db)
    return RapportOut(
        client_id=data["client"].id,
        client_nom=data["client"].nom,
        periode_debut=data["periode_debut"],
        periode_fin=data["periode_fin"],
        n1=data["n1"],
        n2=data["n2"],
        n3=data["n3"],
        heures_supp_minutes=data["heures_supp_minutes"],
        interventions=data["interventions"],
    )


@router.get("/{client_id}/pdf")
def get_rapport_pdf(client_id: int, periode: str = "courante", db: Session = Depends(get_db)):
    data = _get_client_et_rapport(client_id, periode, db)
    pdf_bytes = generer_pdf(data)
    filename = f"rapport_{nom_fichier_sur(data['client'].nom)}_{data['periode_debut']}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{client_id}/xlsx")
def get_rapport_xlsx(client_id: int, periode: str = "courante", db: Session = Depends(get_db)):
    data = _get_client_et_rapport(client_id, periode, db)
    xlsx_bytes = generer_excel(data)
    filename = f"rapport_{nom_fichier_sur(data['client'].nom)}_{data['periode_debut']}.xlsx"
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
