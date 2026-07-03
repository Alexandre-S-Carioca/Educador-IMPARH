import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..infrastructure.db.session import get_db
from ..infrastructure.services.ai_tutor import get_tutor_service, BaseTutorService
from ..domain.schemas import AiExplainRequest, AiExplainResponse
from .progress import get_current_user_id

router = APIRouter(prefix="/ai", tags=["AI Tutor"])

@router.post("/explain", response_model=AiExplainResponse)
async def explain_question(
    request: AiExplainRequest,
    db: Session = Depends(get_db),
    tutor: BaseTutorService = Depends(get_tutor_service),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    try:
        explanation = await tutor.explain(db, request.question_id, request.selected_option)
        # Log action
        try:
            from ..infrastructure.repositories.activity_log_repo import ActivityLogRepository
            from ..infrastructure.db.models.content import Question
            q = db.query(Question).filter(Question.id == request.question_id).first()
            subject_info = f" em '{q.subject}'" if q else ""
            
            repo = ActivityLogRepository(db)
            repo.create_log(user_id=user_id, action="ASK_AI", details=f"Pediu explicação da IA para uma questão{subject_info}")
        except Exception:
            pass
        return AiExplainResponse(explanation_markdown=explanation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
