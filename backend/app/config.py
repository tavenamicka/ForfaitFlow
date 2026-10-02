from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    admin_email: str
    admin_password: str
    tz: str = "Europe/Paris"
    # Défaut sûr : la doc interactive (/docs, /redoc, /openapi.json) ne
    # s'ouvre que si ce champ est explicitement mis à "development" — jamais
    # l'inverse (variable d'environnement ENVIRONMENT).
    environment: str = "production"


settings = Settings()
