from sqlalchemy.orm import Session
from ..db.models.assignment import Assignment
from ...domain.schemas import AssignmentCreate
import uuid
from typing import List

class AssignmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, teacher_id: uuid.UUID, assignment_in: AssignmentCreate) -> Assignment:
        db_assignment = Assignment(
            teacher_id=teacher_id,
            classroom_id=assignment_in.classroom_id,
            title=assignment_in.title,
            type=assignment_in.type,
            description=assignment_in.description,
            due_date=assignment_in.due_date,
            rubric=assignment_in.rubric
        )
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_assignment)
        return db_assignment

    def get(self, assignment_id: uuid.UUID) -> Assignment | None:
        return self.db.query(Assignment).filter(Assignment.id == assignment_id).first()

    def list_by_classroom(self, classroom_id: uuid.UUID) -> List[Assignment]:
        return self.db.query(Assignment).filter(Assignment.classroom_id == classroom_id).all()
