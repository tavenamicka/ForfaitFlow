FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    libpq5 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libcairo2 \
    libffi8 \
    shared-mime-info \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# --proxy-headers / --forwarded-allow-ips : le backend n'est joint que par le
# conteneur `forfaitflow-frontend` (Nginx), qui transmet l'IP visiteur dans
# X-Forwarded-For. 172.16.0.0/12 couvre les réseaux Docker ; sans lui Uvicorn
# ignorerait l'en-tête et le throttle de connexion (app/core/limiter.py)
# verrait toujours la même adresse interne, partagée entre tous les visiteurs.
# Si un reverse proxy placé devant l'application se connecte depuis une autre
# adresse, ajoutez-la à la liste (jamais '*' : l'IP deviendrait forgeable).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "172.16.0.0/12"]
