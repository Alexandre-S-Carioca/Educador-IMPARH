from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
from typing import List

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.unit_repo import UnitRepository
from ..domain.schemas import UnitResponse, UnitBase

router = APIRouter(prefix="/modules/{module_id}/units", tags=["Units"])

@router.post("/", response_model=UnitResponse)
def create_unit(module_id: uuid.UUID, unit_in: UnitBase, db: Session = Depends(get_db)):
    repo = UnitRepository(db)
    return repo.create(module_id, unit_in)

@router.get("/", response_model=List[UnitResponse])
def get_units_by_module(module_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = UnitRepository(db)
    return repo.get_by_module(module_id)
