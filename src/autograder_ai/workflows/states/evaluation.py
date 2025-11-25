from enum import Enum
from typing import List, Dict, Any
from typing_extensions import TypedDict

class EvaluationStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"



class EvalutationState(TypedDict):
    question_id: str
    question: str
    code: str
    test_cases: List[Dict[str, Any]]
    current_test_index: int
    test_results: List[Dict[str, Any]]
    status: EvaluationStatus

