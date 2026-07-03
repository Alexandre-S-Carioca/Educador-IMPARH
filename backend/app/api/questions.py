from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
from typing import List

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.question_repo import QuestionRepository
from ..domain.schemas import QuestionResponse, QuestionBase

router = APIRouter(prefix="/topics/{topic_id}/questions", tags=["Questions"])

@router.post("/", response_model=QuestionResponse)
def create_question(topic_id: uuid.UUID, question_in: QuestionBase, db: Session = Depends(get_db)):
    repo = QuestionRepository(db)
    return repo.create(topic_id, question_in)

@router.get("/", response_model=List[QuestionResponse])
def get_questions_by_topic(topic_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = QuestionRepository(db)
    return repo.get_by_topic(topic_id)
