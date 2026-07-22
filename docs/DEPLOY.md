# Déploiement (self-hosted)

ForfaitFlow est pensé pour être auto-hébergé sur un serveur Linux avec Docker.
Ce guide décrit un déploiement de production type, tel qu'utilisé en réel sur le
serveur de référence (Ubuntu Server + Nginx + Let's Encrypt).

## Prérequis

- Docker + Docker Compose
- Un reverse proxy (Nginx dans cet exemple) avec un certificat TLS valide pour
  le sous-domaine choisi
- Un point de montage disponible pour les sauvegardes (`pg_dump` quotidien)

## 1. Cloner et configurer

```bash
git clone <url-du-repo> forfaitflow
cd forfaitflow
cp .env.example .env
```

Éditer `.env` et renseigner de vraies valeurs :

```bash
DB_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(64))")
ADMIN_EMAIL=vous@exemple.fr
ADMIN_PASSWORD=<mot-de-passe-fort>
```

`.env` n'est jamais committé (voir `.gitignore`).

## 2. Adapter le binding des ports

Le `docker-compose.yml` publie le frontend sur `8092` et l'API sur `8093`. En
production, **ne jamais publier sur `0.0.0.0`** — binder explicitement sur
l'IP LAN du serveur pour ne pas contourner le pare-feu (Docker insère ses
règles iptables en amont d'UFW/nftables) :

```yaml
services:
  forfaitflow-backend:
    ports:
      - "192.168.1.X:8093:8000"
  forfaitflow-frontend:
    ports:
      - "192.168.1.X:8092:80"
```

## 3. Build et démarrage

```bash
docker compose up -d --build
docker compose exec forfaitflow-backend alembic upgrade head
```

Le compte admin (`ADMIN_EMAIL`/`ADMIN_PASSWORD`) est créé automatiquement au
premier démarrage du backend, une fois les migrations appliquées.

Vérifier que tout tourne :

```bash
docker compose ps
curl -I http://192.168.1.X:8092/
curl -I http://192.168.1.X:8093/docs
```

## 4. Reverse proxy Nginx + TLS

Le frontend proxifie déjà `/api/` en interne vers le backend via le réseau
Docker (`frontend/nginx.conf`) — le vhost public n'a donc besoin de pointer
que vers le port frontend.

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name forfaitflow.exemple.fr;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name forfaitflow.exemple.fr;

    ssl_certificate     /etc/letsencrypt/live/exemple.fr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/exemple.fr/privkey.pem;

    location / {
        proxy_pass http://192.168.1.X:8092;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/forfaitflow.exemple.fr /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Certificat obtenu via Certbot (`certbot certonly` ou plugin DNS selon le
registrar) — un certificat wildcard couvrant tous les sous-domaines évite de
relancer Certbot à chaque nouvelle application.

## 5. Sauvegardes

Le service `forfaitflow-backup` du `docker-compose.yml` fait un `pg_dump`
quotidien vers `./backups` (rotation à 30 jours). Montez à la place un volume ou un
point de montage dédié aux sauvegardes si vous le souhaitez (`volumes:` du service).

## 6. Mises à jour

```bash
git pull
docker compose up -d --build
docker compose exec forfaitflow-backend alembic upgrade head
```
