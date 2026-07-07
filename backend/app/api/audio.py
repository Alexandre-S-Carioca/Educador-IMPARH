from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List, Optional

from ..infrastructure.db.session import get_db
from ..infrastructure.db.models.content import AudioContent
from ..domain.schemas import AudioContentResponse

router = APIRouter(prefix="/audio", tags=["Audio"])

@router.get("/topic/{topic_id}", response_model=List[AudioContentResponse])
def get_audio_by_topic(
    topic_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    from ..infrastructure.db.models.course import Topic
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    audios = db.query(AudioContent).filter(AudioContent.topic_id == topic_id).all()
    return audios

@router.post("/", response_model=AudioContentResponse)
def create_audio_content(
    topic_id: uuid.UUID,
    word_or_phrase: str,
    audio_url: str,
    ipa_phonetic: str,
    language_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    from ..infrastructure.db.models.course import Topic
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    db_audio = AudioContent(
        topic_id=topic_id,
        word_or_phrase=word_or_phrase,
        audio_url=audio_url,
        ipa_phonetic=ipa_phonetic,
        language_level=language_level
    )
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio
