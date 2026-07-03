from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.course_repo import CourseRepository
from ..domain.schemas import CourseResponse, CourseCreate

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseResponse)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    return repo.create(course_in)

@router.get("/", response_model=List[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    return repo.list_all()

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    course = repo.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
