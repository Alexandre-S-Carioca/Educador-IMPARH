from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
from typing import List

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.module_repo import ModuleRepository
from ..domain.schemas import ModuleResponse, ModuleBase

router = APIRouter(prefix="/courses/{course_id}/modules", tags=["Modules"])

@router.post("/", response_model=ModuleResponse)
def create_module(course_id: uuid.UUID, module_in: ModuleBase, db: Session = Depends(get_db)):
    repo = ModuleRepository(db)
    return repo.create(course_id, module_in)

@router.get("/", response_model=List[ModuleResponse])
def get_modules_by_course(course_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = ModuleRepository(db)
    return repo.get_by_course(course_id)
