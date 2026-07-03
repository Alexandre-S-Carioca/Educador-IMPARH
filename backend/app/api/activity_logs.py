from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.activity_log_repo import ActivityLogRepository
from ..domain.schemas import ActivityLogCreate, ActivityLogResponse

# Mock validation of current user id (matching project's mock auth standard)
def get_current_user_id() -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_DNS, "mock_student_user")

router = APIRouter(prefix="/activity-logs", tags=["ActivityLogs"])

@router.post("/", response_model=ActivityLogResponse)
def record_log(
    log_in: ActivityLogCreate,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    repo = ActivityLogRepository(db)
    log = repo.create_log(user_id=user_id, action=log_in.action, details=log_in.details)
    return ActivityLogResponse.model_validate(log)

@router.get("/", response_model=List[ActivityLogResponse])
def get_activity_logs(
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
    limit: int = 50
):
    repo = ActivityLogRepository(db)
    logs = repo.list_logs(user_id=user_id, limit=limit)
    return [ActivityLogResponse.model_validate(log) for log in logs]
