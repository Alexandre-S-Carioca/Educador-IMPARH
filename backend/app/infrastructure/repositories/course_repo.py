from sqlalchemy.orm import Session
from ..db.models.course import Course
from ...domain.schemas import CourseCreate
import uuid
from typing import List

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, course_in: CourseCreate) -> Course:
        db_course = Course(name=course_in.name, description=course_in.description)
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def get(self, course_id: uuid.UUID) -> Course | None:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def list_all(self) -> List[Course]:
        return self.db.query(Course).all()
