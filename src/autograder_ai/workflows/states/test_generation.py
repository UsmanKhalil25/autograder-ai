from typing import List, Dict, Any
from typing_extensions import TypedDict

class TestGenerationState(TypedDict):
    question_id: str
    question: str
    code: str
    test_cases: List[Dict[str, Any]]

