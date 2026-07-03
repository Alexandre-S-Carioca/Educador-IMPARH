from sqlalchemy.orm import Session
import uuid
from typing import List
from ..db.models.activity_log import ActivityLog

class ActivityLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_log(self, user_id: uuid.UUID, action: str, details: str | None = None) -> ActivityLog:
        db_log = ActivityLog(user_id=user_id, action=action, details=details)
        self.db.add(db_log)
        self.db.commit()
        self.db.refresh(db_log)
        return db_log

    def list_logs(self, user_id: uuid.UUID, limit: int = 50) -> List[ActivityLog]:
        return self.db.query(ActivityLog).filter(ActivityLog.user_id == user_id).order_by(ActivityLog.created_at.desc()).limit(limit).all()
