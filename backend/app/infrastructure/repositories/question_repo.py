from sqlalchemy.orm import Session
from ..db.models.content import Question
from ...domain.schemas import QuestionBase
import uuid
from typing import List

class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, topic_id: uuid.UUID, question_in: QuestionBase) -> Question:
        db_question = Question(
            topic_id=topic_id,
            statement=question_in.statement,
            option_a=question_in.option_a,
            option_b=question_in.option_b,
            option_c=question_in.option_c,
            option_d=question_in.option_d,
            correct_option=question_in.correct_option,
            justification_correct=question_in.justification_correct,
            justification_incorrect=question_in.justification_incorrect,
            difficulty=question_in.difficulty,
            subject=question_in.subject,
            subsubject=question_in.subsubject,
            board=question_in.board,
            keywords=question_in.keywords
        )
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return db_question

    def get_by_topic(self, topic_id: uuid.UUID) -> List[Question]:
        return self.db.query(Question).filter(Question.topic_id == topic_id).all()
