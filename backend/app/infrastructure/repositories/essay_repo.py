from sqlalchemy.orm import Session
from ..db.models.essay import StudentEssay, StudentSubmission
from ...domain.schemas import StudentEssayCreate, StudentSubmissionCreate
import uuid
from typing import List, Optional

class EssayRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_essay(self, student_id: uuid.UUID, essay_in: StudentEssayCreate) -> StudentEssay:
        # Contagem de palavras simples por espaços
        words = essay_in.content.split()
        word_count = len(words)

        db_essay = StudentEssay(
            student_id=student_id,
            assignment_id=essay_in.assignment_id,
            content=essay_in.content,
            word_count=word_count,
            status="submitted" if essay_in.assignment_id else "draft"
        )
        self.db.add(db_essay)
        self.db.commit()
        self.db.refresh(db_essay)
        return db_essay

    def get_essay(self, essay_id: uuid.UUID) -> StudentEssay | None:
        return self.db.query(StudentEssay).filter(StudentEssay.id == essay_id).first()

    def list_essays_by_student(self, student_id: uuid.UUID) -> List[StudentEssay]:
        return self.db.query(StudentEssay).filter(StudentEssay.student_id == student_id).all()

    def update_essay_feedback(self, essay_id: uuid.UUID, grade: float, teacher_feedback: str) -> StudentEssay | None:
        db_essay = self.get_essay(essay_id)
        if db_essay:
            db_essay.grade = grade
            db_essay.teacher_feedback = teacher_feedback
            db_essay.status = "graded"
            self.db.commit()
            self.db.refresh(db_essay)
        return db_essay

    def create_submission(self, student_id: uuid.UUID, sub_in: StudentSubmissionCreate) -> StudentSubmission:
        import datetime
        db_submission = StudentSubmission(
            student_id=student_id,
            assignment_id=sub_in.assignment_id,
            content=sub_in.content,
            submitted_at=datetime.datetime.utcnow()
        )
        self.db.add(db_submission)
        self.db.commit()
        self.db.refresh(db_submission)
        return db_submission

    def get_submission(self, sub_id: uuid.UUID) -> StudentSubmission | None:
        return self.db.query(StudentSubmission).filter(StudentSubmission.id == sub_id).first()

    def list_submissions_by_assignment(self, assignment_id: uuid.UUID) -> List[StudentSubmission]:
        return self.db.query(StudentSubmission).filter(StudentSubmission.assignment_id == assignment_id).all()
