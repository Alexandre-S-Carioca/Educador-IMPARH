from sqlalchemy.orm import Session
from ..db.models.classroom import ClassRoom
from ...domain.schemas import ClassRoomCreate
import uuid
from typing import List

class ClassRoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, teacher_id: uuid.UUID, classroom_in: ClassRoomCreate) -> ClassRoom:
        db_classroom = ClassRoom(
            teacher_id=teacher_id,
            name=classroom_in.name,
            level=classroom_in.level,
            series=classroom_in.series
        )
        self.db.add(db_classroom)
        self.db.commit()
        self.db.refresh(db_classroom)
        return db_classroom

    def get(self, classroom_id: uuid.UUID) -> ClassRoom | None:
        return self.db.query(ClassRoom).filter(ClassRoom.id == classroom_id).first()

    def list_by_teacher(self, teacher_id: uuid.UUID) -> List[ClassRoom]:
        return self.db.query(ClassRoom).filter(ClassRoom.teacher_id == teacher_id).all()

    def add_student_to_classroom(self, classroom_id: uuid.UUID, student_id: uuid.UUID) -> bool:
        from ..db.models.user import User
        db_classroom = self.get(classroom_id)
        # Note: corrigido de ..infrastructure.db.models.user para ..db.models.user
        db_student = self.db.query(User).filter(User.id == student_id).first()
        if db_classroom and db_student:
            db_student.classroom_id = classroom_id
            self.db.commit()
            return True
        return False

    def get_classroom_stats(self, classroom_id: uuid.UUID) -> dict | None:
        from ..db.models.user import User
        from ..db.models.assignment import Assignment
        from ..db.models.essay import StudentEssay
        from sqlalchemy import func

        classroom = self.get(classroom_id)
        if not classroom:
            return None

        # 1. Total de estudantes
        students_count = self.db.query(User).filter(User.classroom_id == classroom_id).count()

        # 2. Obter todas as tarefas da sala
        assignments = self.db.query(Assignment).filter(Assignment.classroom_id == classroom_id).all()
        assignments_stats = []

        for assignment in assignments:
            # Quantos enviaram redação para esta tarefa
            submissions_count = self.db.query(StudentEssay).filter(
                StudentEssay.assignment_id == assignment.id,
                StudentEssay.status.in_(["submitted", "reviewed", "graded"])
            ).count()

            # Porcentagem de entrega
            submissions_percentage = 0.0
            if students_count > 0:
                submissions_percentage = round((submissions_count / students_count) * 100, 2)

            # Média de notas
            average_grade = self.db.query(func.avg(StudentEssay.grade)).filter(
                StudentEssay.assignment_id == assignment.id,
                StudentEssay.grade != None
            ).scalar()

            if average_grade is not None:
                average_grade = round(float(average_grade), 2)

            assignments_stats.append({
                "assignment_id": assignment.id,
                "title": assignment.title,
                "submissions_count": submissions_count,
                "submissions_percentage": submissions_percentage,
                "average_grade": average_grade
            })

        return {
            "classroom_id": classroom.id,
            "name": classroom.name,
            "students_count": students_count,
            "assignments_stats": assignments_stats
        }
