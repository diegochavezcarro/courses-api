from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    responses={404: {"description": "Not found"}},
)

async def get_db():
    async with SessionLocal() as db:
        yield db

@router.get("/", response_model=List[schemas.Course])
async def read_courses(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    courses = await crud.get_courses(db, skip=skip, limit=limit)
    return courses

@router.post("/", response_model=schemas.Course)
async def create_course(course: schemas.CourseCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_course(db=db, course=course)

@router.get("/{course_id}", response_model=schemas.Course)
async def read_course(course_id: int, db: AsyncSession = Depends(get_db)):
    db_course = await crud.get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.delete("/{course_id}")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete_course(db=db, course_id=course_id)
    return {"message": "Course deleted"}



