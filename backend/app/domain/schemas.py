from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid
from datetime import datetime

class TopicBase(BaseModel):
    title: str
    difficulty: int
    order_index: int
    objectives: Optional[str] = None
    introduction: Optional[str] = None
    theory_markdown: Optional[str] = None

class TopicCreate(TopicBase):
    pass

class QuestionBase(BaseModel):
    statement: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    justification_correct: str
    justification_incorrect: str
    difficulty: int = 1
    subject: str
    subsubject: str
    board: str = "IMPARH"
    keywords: Optional[Dict] = None

class QuestionResponse(QuestionBase):
    id: uuid.UUID
    topic_id: uuid.UUID
    model_config = {"from_attributes": True}

class FlashcardBase(BaseModel):
    front: str
    back: str

class FlashcardResponse(FlashcardBase):
    id: uuid.UUID
    topic_id: uuid.UUID
    model_config = {"from_attributes": True}

class ExampleBase(BaseModel):
    content: str
    is_commented: bool = False

class ExampleResponse(ExampleBase):
    id: uuid.UUID
    topic_id: uuid.UUID
    model_config = {"from_attributes": True}

class TopicResponse(TopicBase):
    id: uuid.UUID
    unit_id: uuid.UUID
    
    questions: List[QuestionResponse] = []
    flashcards: List[FlashcardResponse] = []
    examples: List[ExampleResponse] = []

    model_config = {"from_attributes": True}

class UnitBase(BaseModel):
    title: str
    order_index: int

class UnitResponse(UnitBase):
    id: uuid.UUID
    module_id: uuid.UUID
    topics: List[TopicResponse] = []

    model_config = {"from_attributes": True}

class ModuleBase(BaseModel):
    title: str
    order_index: int

class ModuleResponse(ModuleBase):
    id: uuid.UUID
    course_id: uuid.UUID
    units: List[UnitResponse] = []

    model_config = {"from_attributes": True}

class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: uuid.UUID
    modules: List[ModuleResponse] = []

    model_config = {"from_attributes": True}

class AttemptCreate(BaseModel):
    question_id: uuid.UUID
    is_correct: bool

class AttemptResponse(BaseModel):
    id: uuid.UUID
    xp_awarded: int
    is_correct: bool

    model_config = {"from_attributes": True}

class ProgressSummary(BaseModel):
    user_id: uuid.UUID
    total_xp: int
    level: int
    
    model_config = {"from_attributes": True}

class AiExplainRequest(BaseModel):
    question_id: uuid.UUID
    selected_option: str # Ex: "A", "B"

class AiExplainResponse(BaseModel):
    explanation_markdown: str

class FlashcardBase(BaseModel):
    front: str
    back: str

class FlashcardResponse(FlashcardBase):
    id: uuid.UUID
    topic_id: uuid.UUID
    
    model_config = {"from_attributes": True}

class UserStatisticsSummary(BaseModel):
    total_questions: int
    total_correct: int
    total_incorrect: int
    accuracy_percentage: float

class ActivityLogCreate(BaseModel):
    action: str
    details: Optional[str] = None

class ActivityLogResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    action: str
    details: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
