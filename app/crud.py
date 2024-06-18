from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas

async def get_course(db: AsyncSession, course_id: int):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    return result.scalars().first()

async def get_courses(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[models.Course]:
    result = await db.execute(select(models.Course).offset(skip).limit(limit))
    return result.scalars().all()

async def create_course(db: AsyncSession, course: schemas.CourseCreate):
    db_course = models.Course(name=course.name, description=course.description)
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

async def delete_course(db: AsyncSession, course_id: int):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    db_course = result.scalars().first()
    if db_course:
        await db.delete(db_course)
        await db.commit()
