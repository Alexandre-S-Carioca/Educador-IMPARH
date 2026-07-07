from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.assignment_repo import AssignmentRepository
from ..domain.schemas import AssignmentCreate, AssignmentResponse
from .classrooms import get_current_teacher_id

router = APIRouter(prefix="/assignments", tags=["Assignments"])

@router.post("/", response_model=AssignmentResponse)
def create_assignment(
    assignment_in: AssignmentCreate,
    db: Session = Depends(get_db),
    teacher_id: uuid.UUID = Depends(get_current_teacher_id)
):
    # Verificar se a turma existe
    from ..infrastructure.repositories.classroom_repo import ClassRoomRepository
    class_repo = ClassRoomRepository(db)
    classroom = class_repo.get(assignment_in.classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    repo = AssignmentRepository(db)
    return repo.create(teacher_id, assignment_in)

@router.get("/{assignment_id}", response_model=AssignmentResponse)
def get_assignment(
    assignment_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    repo = AssignmentRepository(db)
    assignment = repo.get(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.get("/classroom/{classroom_id}", response_model=List[AssignmentResponse])
def get_assignments_by_classroom(
    classroom_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    repo = AssignmentRepository(db)
    return repo.list_by_classroom(classroom_id)
