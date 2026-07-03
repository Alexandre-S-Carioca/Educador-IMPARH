from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.progress_repo import ProgressRepository
from ..domain.schemas import AttemptCreate, AttemptResponse, ProgressSummary, UserStatisticsSummary

# Mock de autenticação para retornar sempre um ID de usuário fixo por enquanto
def get_current_user_id() -> uuid.UUID:
    # Usando o namespace DNS UUID para gerar sempre o mesmo UUID "mock"
    return uuid.uuid5(uuid.NAMESPACE_DNS, "mock_student_user")

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.post("/attempt", response_model=AttemptResponse)
def record_question_attempt(
    attempt_in: AttemptCreate, 
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    repo = ProgressRepository(db)
    attempt = repo.record_attempt(user_id, attempt_in)
    return AttemptResponse.model_validate(attempt)

@router.get("/summary", response_model=ProgressSummary)
def get_progress_summary(
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    repo = ProgressRepository(db)
    summary = repo.get_summary(user_id)
    return ProgressSummary.model_validate(summary)

@router.get("/stats", response_model=UserStatisticsSummary)
def get_user_statistics(
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    repo = ProgressRepository(db)
    return repo.get_user_statistics(user_id)

