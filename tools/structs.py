from pydantic import BaseModel
from enum import Enum

class FicticiousPassage(BaseModel):
    summary: str
    passage: str
    
class FicticiousEntry(BaseModel):
    new_question: str
    new_answer: str
    new_short_answer: str
    answer_contexts: list[FicticiousPassage]
    false_short_answers: list[str]
    generation_review: str
    contained_contradictions: bool
    
class SynthNQEntry(BaseModel):
    id: str
    question: str
    answer: str
    short_answer: str
    passages: list[FicticiousPassage]
    false_answers: list[str]
    
class QuestionType(str, Enum):
    HISTORY = "HISTORY"
    GEOGRAPHY = "GEOGRAPHY"
    SCIENCE = "SCIENCE"
    TECHNOLOGY = "TECHNOLOGY"
    ENTERTAINMENT = "ENTERTAINMENT"
    SPORTS = "SPORTS"
    POP_CULTURE = "POP_CULTURE"
    FICTION = "FICTION"
    BIOLOGY = "BIOLOGY"
    ANCIENT_HISTORY = "ANCIENT_HISTORY"
    RECENT_HISTORY = "RECENT_HISTORY"
    POLITICS = "POLITICS"
    ART = "ART"
    MUSIC = "MUSIC"
    LITERATURE = "LITERATURE"
    FILM = "FILM"