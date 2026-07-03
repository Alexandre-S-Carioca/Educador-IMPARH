from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
import uuid
from typing import List

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.topic_repo import TopicRepository
from ..domain.schemas import TopicResponse, TopicCreate

router = APIRouter(prefix="/units/{unit_id}/topics", tags=["Topics"])
global_router = APIRouter(prefix="/topics", tags=["Topics"])

@router.post("/", response_model=TopicResponse)
def create_topic(unit_id: uuid.UUID, topic_in: TopicCreate, db: Session = Depends(get_db)):
    repo = TopicRepository(db)
    return repo.create(unit_id, topic_in)

@router.get("/", response_model=List[TopicResponse])
def get_topics_by_unit(unit_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = TopicRepository(db)
    return repo.get_by_unit(unit_id)

@global_router.get("/{topic_id}", response_model=TopicResponse)
def get_topic_with_content(topic_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = TopicRepository(db)
    topic = repo.get_by_id_with_content(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic
