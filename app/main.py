from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import courses
from app.database import database, create_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform startup actions
    await database.connect()
    await create_db()
    yield
    # Perform shutdown actions if needed
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(courses.router)


