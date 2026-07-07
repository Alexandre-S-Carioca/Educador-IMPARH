from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.essay_repo import EssayRepository
from ..infrastructure.repositories.assignment_repo import AssignmentRepository
from ..infrastructure.services.ai_tutor import get_tutor_service, BaseTutorService
from ..domain.schemas import StudentEssayCreate, StudentEssayResponse
from .progress import get_current_user_id

router = APIRouter(prefix="/essays", tags=["Essays"])

@router.post("/", response_model=StudentEssayResponse)
async def submit_essay(
    essay_in: StudentEssayCreate,
    db: Session = Depends(get_db),
    student_id: uuid.UUID = Depends(get_current_user_id),
    ai_service: BaseTutorService = Depends(get_tutor_service)
):
    # 1. Obter título e rubrica
    title = "Treino Livre de Redação"
    rubric = None
    if essay_in.assignment_id:
        assign_repo = AssignmentRepository(db)
        assignment = assign_repo.get(essay_in.assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        title = assignment.title
        rubric = assignment.rubric

    # 2. Criar a redação no banco (calcula contagem de palavras)
    repo = EssayRepository(db)
    db_essay = repo.create_essay(student_id, essay_in)

    # 3. Invocar IA para correção automática
    grade, feedback = await ai_service.correct_essay(db_essay.content, title, rubric)
    
    # 4. Atualizar no banco com o feedback da IA
    db_essay.grade = grade
    db_essay.ai_feedback = feedback
    db_essay.status = "reviewed"
    db.commit()
    db.refresh(db_essay)

    # Log action
    try:
        from ..infrastructure.repositories.activity_log_repo import ActivityLogRepository
        log_repo = ActivityLogRepository(db)
        log_repo.create_log(user_id=student_id, action="SUBMIT_ESSAY", details=f"Enviou a redação '{title}' para correção (nota: {grade})")
    except Exception:
        pass

    return db_essay

@router.get("/", response_model=List[StudentEssayResponse])
def get_student_essays(
    all_essays: bool = False,
    db: Session = Depends(get_db),
    student_id: uuid.UUID = Depends(get_current_user_id)
):
    repo = EssayRepository(db)
    if all_essays:
        from ..infrastructure.db.models.essay import StudentEssay
        return db.query(StudentEssay).all()
    return repo.list_essays_by_student(student_id)

@router.get("/{essay_id}", response_model=StudentEssayResponse)
def get_essay_details(
    essay_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    repo = EssayRepository(db)
    essay = repo.get_essay(essay_id)
    if not essay:
        raise HTTPException(status_code=404, detail="Essay not found")
    return essay

@router.put("/{essay_id}/feedback", response_model=StudentEssayResponse)
def update_teacher_feedback(
    essay_id: uuid.UUID,
    grade: float,
    teacher_feedback: str,
    db: Session = Depends(get_db)
):
    repo = EssayRepository(db)
    essay = repo.update_essay_feedback(essay_id, grade, teacher_feedback)
    if not essay:
        raise HTTPException(status_code=404, detail="Essay not found")
    return essay
