from core.Settings import settings
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from db.models.Base import Base
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from asyncio import sleep
from db.session import engine
from api.base import api_router
from db.models.Car import Car #Used to Create table
from db.models.Booking import Booking #Used to Create table

def create_tables():
    print ("Creating tables...", flush=True)
    Base.metadata.create_all(bind=engine)


def include_router(app: FastAPI):
    app.include_router(api_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    count = 0
    while True:
        count += 1
        try:
            engine = create_engine(settings.DB_URL.unicode_string())
            connection = engine.connect()
            result = connection.execute(text("SELECT VERSION()"))
            version = result.scalar()
            print(f"Connection successful. MySQL Server Version: {version}", flush=True)
            connection.close()
            create_tables()
            break
        except OperationalError as e:
            print(f"Failed to connect to the MySQL server #{count}: {e}", flush=True)
            await sleep(1)
    yield

def start_application():
    print("--------------------CAR_RENTAL SERVER--------------------")
    app = FastAPI(title=f"{settings.PROJECT_NAME}",
                  version=settings.PROJECT_VERSION,
                  lifespan=lifespan)
    
    include_router(app)

    from fastapi import __version__ as fastapi_version
    from pydantic import __version__ as pydantic_version
    from sqlalchemy import __version__ as sqlalchemy_version
    from datetime import date
    print(f"Today: {date.today()}")
    print(f"FastAPI version: {fastapi_version}", flush=True)
    print(f"pydantic version: {pydantic_version}", flush=True)
    print(f"sqlAlchemy version: {sqlalchemy_version}", flush=True)

    return app

app = start_application()


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse("/docs")