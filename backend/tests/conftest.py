import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.infrastructure.db.models import Base
from app.infrastructure.db.session import get_db
import os

# Usamos um banco de dados SQLite em memória ou arquivo local para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    # Cria as tabelas antes dos testes
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        # Dropa as tabelas após os testes
        Base.metadata.drop_all(bind=engine)
        # Libera todas as conexões do pool antes de deletar (necessário no Windows)
        engine.dispose()
        if os.path.exists("./test.db"):
            os.remove("./test.db")

@pytest.fixture(scope="module")
def client(db):
    # Substitui a dependência do banco de dados no FastAPI pelo nosso banco de teste
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
