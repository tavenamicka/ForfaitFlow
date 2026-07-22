"""Réinitialisation manuelle du mot de passe d'un utilisateur (procédure de secours).

Usage :
    docker compose exec forfaitflow-backend python -m app.scripts.reset_password <email> <nouveau_mot_de_passe>
"""

import sys

from app.core.security import hash_password
from app.database import SessionLocal
from app.models.user import User


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python -m app.scripts.reset_password <email> <nouveau_mot_de_passe>")
        sys.exit(1)

    email, nouveau_mot_de_passe = sys.argv[1], sys.argv[2]
    if len(nouveau_mot_de_passe) < 8:
        print("Le mot de passe doit faire au moins 8 caractères.")
        sys.exit(1)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            print(f"Aucun utilisateur avec l'email {email}")
            sys.exit(1)
        user.hash_password = hash_password(nouveau_mot_de_passe)
        db.commit()
        print(f"Mot de passe réinitialisé pour {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
