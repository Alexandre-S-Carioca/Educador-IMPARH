from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.classroom_repo import ClassRoomRepository
from ..domain.schemas import ClassRoomCreate, ClassRoomResponse, ClassroomStatsResponse
from .progress import get_current_user_id

router = APIRouter(prefix="/classrooms", tags=["Classrooms"])

# Mock do ID do professor para fins de desenvolvimento local
def get_current_teacher_id() -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_DNS, "mock_teacher_user")

@router.post("/", response_model=ClassRoomResponse)
def create_classroom(
    classroom_in: ClassRoomCreate,
    db: Session = Depends(get_db),
    teacher_id: uuid.UUID = Depends(get_current_teacher_id)
):
    # Garantir que o professor exista no banco (se não existir, cria um mock)
    from ..infrastructure.db.models.user import User, UserRole
    teacher = db.query(User).filter(User.id == teacher_id).first()
    if not teacher:
        teacher = User(
            id=teacher_id,
            email="professor@educador.com",
            password_hash="mock_hash",
            role=UserRole.TEACHER
        )
        db.add(teacher)
        db.commit()

    repo = ClassRoomRepository(db)
    return repo.create(teacher_id, classroom_in)

@router.get("/", response_model=List[ClassRoomResponse])
def get_classrooms(
    db: Session = Depends(get_db),
    teacher_id: uuid.UUID = Depends(get_current_teacher_id)
):
    repo = ClassRoomRepository(db)
    return repo.list_by_teacher(teacher_id)

@router.get("/{classroom_id}", response_model=ClassRoomResponse)
def get_classroom(
    classroom_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    repo = ClassRoomRepository(db)
    classroom = repo.get(classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return classroom

@router.post("/{classroom_id}/students/{student_id}")
def add_student(
    classroom_id: uuid.UUID,
    student_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    repo = ClassRoomRepository(db)
    success = repo.add_student_to_classroom(classroom_id, student_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add student. Verify if classroom and student exist.")
    return {"message": "Student successfully added to classroom"}

@router.get("/{classroom_id}/stats", response_model=ClassroomStatsResponse)
def get_classroom_stats_endpoint(
    classroom_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    repo = ClassRoomRepository(db)
    stats = repo.get_classroom_stats(classroom_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return stats
