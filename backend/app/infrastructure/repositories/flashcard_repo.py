from typing import List
import uuid
from sqlalchemy.orm import Session
from ..db.models.content import Flashcard
from ...domain.schemas import FlashcardBase

class FlashcardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_topic(self, topic_id: uuid.UUID) -> List[Flashcard]:
        return self.db.query(Flashcard).filter(Flashcard.topic_id == topic_id).all()

    def create(self, topic_id: uuid.UUID, flashcard_in: FlashcardBase) -> Flashcard:
        flashcard = Flashcard(
            topic_id=topic_id,
            front=flashcard_in.front,
            back=flashcard_in.back
        )
        self.db.add(flashcard)
        self.db.commit()
        self.db.refresh(flashcard)
        return flashcard
