from datetime import date

import pytest

from app.database import SessionLocal
from app.models.client import Client
from app.models.intervention import Intervention


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def make_client(db):
    created = []

    def _make_client(**kwargs):
        defaults = {"nom": "__test_client__", "date_debut_contrat": date(2025, 3, 15)}
        defaults.update(kwargs)
        client = Client(**defaults)
        db.add(client)
        db.commit()
        db.refresh(client)
        created.append(client)
        return client

    yield _make_client

    for client in created:
        db.query(Intervention).filter(Intervention.client_id == client.id).delete()
        db.query(Client).filter(Client.id == client.id).delete()
    db.commit()
