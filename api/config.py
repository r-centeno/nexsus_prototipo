import os

class Config:
    # Pega a URL do Supabase. Se não existir, usa SQLite local.
    uri = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    
    # Fix para SQLAlchemy (Supabase usa postgres://, SQLAlchemy pede postgresql://)
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key")