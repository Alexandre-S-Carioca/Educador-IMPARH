from sqlalchemy.orm import Session
from ..db.models.course import Module
from ...domain.schemas import ModuleBase
import uuid
from typing import List

class ModuleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, course_id: uuid.UUID, module_in: ModuleBase) -> Module:
        db_module = Module(
            course_id=course_id,
            title=module_in.title,
            order_index=module_in.order_index
        )
        self.db.add(db_module)
        self.db.commit()
        self.db.refresh(db_module)
        return db_module

    def get_by_course(self, course_id: uuid.UUID) -> List[Module]:
        return self.db.query(Module).filter(Module.course_id == course_id).order_by(Module.order_index).all()
