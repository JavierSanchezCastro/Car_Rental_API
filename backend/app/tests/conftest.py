import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.session import get_session
from fastapi import FastAPI
from api.base import api_router
from sqlalchemy_utils import create_database, drop_database, database_exists
from db.models.Base import Base
from db.models.Car import Car
from core.Settings import settings

TEST_DATABASE_URL = (
    f"mysql+pymysql://root:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/test_db"
)

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    if database_exists(TEST_DATABASE_URL):
        drop_database(TEST_DATABASE_URL)
    create_database(TEST_DATABASE_URL)
    yield
    drop_database(TEST_DATABASE_URL)


@pytest.fixture(scope="function", autouse=True)
def app():
    print("Creating tables...", flush=True)
    Base.metadata.create_all(bind=test_engine)
    app = FastAPI()
    app.include_router(api_router)
    yield app
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function", autouse=True)
def sample_car(db_session):
    car = Car(
        brand="Toyota",
        model="Corolla",
        type="standard",
        year=2022,
        price_per_day=50
    )
    db_session.add(car)
    db_session.commit()
    db_session.refresh(car)
    return car


@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_session] = override_get_db

    with TestClient(app) as c:
        yield c

