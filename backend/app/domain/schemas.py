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


# Esquemas da v2.0
from ..infrastructure.db.models.user import UserLevel

class ClassRoomBase(BaseModel):
    name: str
    level: UserLevel
    series: int

class ClassRoomCreate(ClassRoomBase):
    pass

class ClassRoomResponse(ClassRoomBase):
    id: uuid.UUID
    teacher_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AssignmentBase(BaseModel):
    title: str
    type: str  # "essay" | "quiz" | "exercise"
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    rubric: Optional[Dict] = None

class AssignmentCreate(AssignmentBase):
    classroom_id: uuid.UUID

class AssignmentResponse(AssignmentBase):
    id: uuid.UUID
    teacher_id: uuid.UUID
    classroom_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StudentEssayBase(BaseModel):
    content: str

class StudentEssayCreate(StudentEssayBase):
    assignment_id: Optional[uuid.UUID] = None

class StudentEssayResponse(StudentEssayBase):
    id: uuid.UUID
    student_id: uuid.UUID
    assignment_id: Optional[uuid.UUID]
    word_count: int
    grade: Optional[float]
    ai_feedback: Optional[str]
    teacher_feedback: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StudentSubmissionBase(BaseModel):
    content: Optional[str] = None

class StudentSubmissionCreate(StudentSubmissionBase):
    assignment_id: uuid.UUID

class StudentSubmissionResponse(StudentSubmissionBase):
    id: uuid.UUID
    assignment_id: uuid.UUID
    student_id: uuid.UUID
    submitted_at: Optional[datetime]
    grade: Optional[float]
    feedback: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class AssignmentStat(BaseModel):
    assignment_id: uuid.UUID
    title: str
    submissions_count: int
    submissions_percentage: float
    average_grade: Optional[float]

    model_config = {"from_attributes": True}

class ClassroomStatsResponse(BaseModel):
    classroom_id: uuid.UUID
    name: str
    students_count: int
    assignments_stats: List[AssignmentStat] = []

    model_config = {"from_attributes": True}

class AudioContentResponse(BaseModel):
    id: uuid.UUID
    topic_id: uuid.UUID
    word_or_phrase: str
    audio_url: Optional[str] = None
    ipa_phonetic: Optional[str] = None
    language_level: Optional[str] = None

    model_config = {"from_attributes": True}







