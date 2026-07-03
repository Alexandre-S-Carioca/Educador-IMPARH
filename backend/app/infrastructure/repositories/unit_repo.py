from sqlalchemy.orm import Session
from ..db.models.course import Unit
from ...domain.schemas import UnitBase
import uuid
from typing import List

class UnitRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, module_id: uuid.UUID, unit_in: UnitBase) -> Unit:
        db_unit = Unit(
            module_id=module_id,
            title=unit_in.title,
            order_index=unit_in.order_index
        )
        self.db.add(db_unit)
        self.db.commit()
        self.db.refresh(db_unit)
        return db_unit

    def get_by_module(self, module_id: uuid.UUID) -> List[Unit]:
        return self.db.query(Unit).filter(Unit.module_id == module_id).order_by(Unit.order_index).all()
