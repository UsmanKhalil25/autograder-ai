from enum import Enum
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict


class EvaluationStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class TestResult(TypedDict):
    """Schema for a single test execution result"""
    test_index: int
    description: str
    input: Dict[str, Any]
    expected_output: Any
    actual_output: Optional[str]
    passed: bool
    reasoning: str
    execution_error: Optional[str]
    execution_time: Optional[float]


class TestExecutionState(TypedDict):
    """State for the test execution workflow"""
    question_id: str
    code: str
    code_file_path: str
    test_cases: List[Dict[str, Any]]
    current_test_index: int
    test_results: List[TestResult]
    status: EvaluationStatus


class EvalutationState(TypedDict):
    question_id: str
    question: str
    code: str
    test_cases: List[Dict[str, Any]]
    current_test_index: int
    test_results: List[Dict[str, Any]]
    status: EvaluationStatus

