from pathlib import Path
from typing import Dict, Any

from .core.pre_processors.assignment import AssignmentPreProcessor
from .core.pre_processors.submission import SubmissionPreProcessor
from .workflows.builders.test_generation import TestGenerationBuilder
from .clients.openai_client import OpenaiClient


class EvaluationEngine:
    def __init__(self, assignment_path: Path, submission_path: Path):
        self.assignment_path = assignment_path
        self.submission_path = submission_path
        self.results = {}

        openai_client = OpenaiClient()
        self.llm = openai_client.llm

        self.assignment_processor = AssignmentPreProcessor(str(assignment_path))
        self.submission_processor = SubmissionPreProcessor(str(submission_path))

    def _generate_tests(self) -> Dict[str, Any]:
        questions = self.assignment_processor.run()
        submissions = self.submission_processor.run()

        builder = TestGenerationBuilder(self.llm)
        workflow = builder.build()

        for question_id in questions:
            submission_file = None
            for filename in submissions:
                if filename.startswith(question_id):
                    submission_file = filename
                    break

            if not submission_file:
                print(f"No submission found for {question_id}")
                continue

            print(f"\nProcessing {question_id}...")

            # Run workflow
            state = {
                "question_id": question_id,
                "question": questions[question_id],
                "code": submissions[submission_file],
                "test_cases": []
            }

            result = workflow.invoke(state)
            self.results[question_id] = result

        return self.results

    def run(self):
        return self._generate_tests()

