from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db.models.gamification import UserProgress, QuestionAttempt
from ...domain.schemas import AttemptCreate
import uuid

class ProgressRepository:
    def __init__(self, db: Session):
        self.db = db

    def _calculate_level(self, xp: int) -> int:
        # Lógica simples de level: 100 XP por level
        return max(1, (xp // 100) + 1)

    def record_attempt(self, user_id: uuid.UUID, attempt_in: AttemptCreate) -> QuestionAttempt:
        xp_awarded = 10 if attempt_in.is_correct else 0
        
        attempt = QuestionAttempt(
            user_id=user_id,
            question_id=attempt_in.question_id,
            is_correct=attempt_in.is_correct,
            xp_awarded=xp_awarded
        )
        self.db.add(attempt)
        
        # Atualiza o UserProgress
        progress = self.db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        if not progress:
            progress = UserProgress(user_id=user_id, total_xp=0, level=1)
            self.db.add(progress)
            
        progress.total_xp += xp_awarded
        progress.level = self._calculate_level(progress.total_xp)

        # Registra no histórico de ações
        try:
            from ..db.models.activity_log import ActivityLog
            from ..db.models.content import Question
            q = self.db.query(Question).filter(Question.id == attempt_in.question_id).first()
            subject_info = f" em '{q.subject}'" if q else ""
            status_str = "corretamente" if attempt_in.is_correct else "incorretamente"
            xp_str = f" (+{xp_awarded} XP)" if xp_awarded > 0 else ""
            details = f"Respondeu {status_str} a uma questão{subject_info}{xp_str}"
            
            log = ActivityLog(user_id=user_id, action="SUBMIT_ANSWER", details=details)
            self.db.add(log)
        except Exception:
            # Não impede o salvamento do progresso em caso de erro na gravação de logs
            pass
        
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def get_summary(self, user_id: uuid.UUID) -> UserProgress:
        progress = self.db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        if not progress:
            progress = UserProgress(user_id=user_id, total_xp=0, level=1)
            self.db.add(progress)
            self.db.commit()
            self.db.refresh(progress)
        return progress

    def get_user_statistics(self, user_id: uuid.UUID) -> dict:
        total = self.db.query(func.count(QuestionAttempt.id)).filter(QuestionAttempt.user_id == user_id).scalar() or 0
        correct = self.db.query(func.count(QuestionAttempt.id)).filter(QuestionAttempt.user_id == user_id, QuestionAttempt.is_correct == True).scalar() or 0
        
        return {
            "total_questions": total,
            "total_correct": correct,
            "total_incorrect": total - correct,
            "accuracy_percentage": (correct / total * 100) if total > 0 else 0.0
        }
