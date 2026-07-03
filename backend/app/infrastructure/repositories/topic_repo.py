from sqlalchemy.orm import Session, joinedload
from ..db.models.course import Topic
from ...domain.schemas import TopicCreate
import uuid
from typing import List

class TopicRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_with_content(self, topic_id: uuid.UUID) -> Topic:
        return self.db.query(Topic).options(
            joinedload(Topic.questions),
            joinedload(Topic.flashcards),
            joinedload(Topic.examples)
        ).filter(Topic.id == topic_id).first()

    def create(self, unit_id: uuid.UUID, topic_in: TopicCreate) -> Topic:
        db_topic = Topic(
            unit_id=unit_id,
            title=topic_in.title,
            difficulty=topic_in.difficulty,
            order_index=topic_in.order_index,
            objectives=topic_in.objectives,
            introduction=topic_in.introduction
        )
        self.db.add(db_topic)
        self.db.commit()
        self.db.refresh(db_topic)
        return db_topic

    def get_by_unit(self, unit_id: uuid.UUID) -> List[Topic]:
        return self.db.query(Topic).filter(Topic.unit_id == unit_id).order_by(Topic.order_index).all()
