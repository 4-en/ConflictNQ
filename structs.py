from pydantic import BaseModel

class FicticiousPassage(BaseModel):
    summary: str
    passage: str
    
class FicticiousEntry(BaseModel):
    cleaned_question: str
    real_short_answer: str
    new_answer: str
    new_short_answer: str
    answer_contexts: list[FicticiousPassage]
    generation_review: str
    issues_found: bool
    
class Passage(BaseModel):
    passage: str
    summary: str
    
class ConflictNQEntry(BaseModel):
    id: str
    question: str
    cleaned_question: str
    real_answer: str
    real_short_answer: str
    real_passages: list[Passage]
    fake_answer: str
    fake_short_answer: str
    fake_passages: list[Passage]
