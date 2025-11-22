from .core.pre_processors import SubmissionPreProcessor, AssignmentPreProcessor


class Engine:

    def __init__(self, assignment_path: str, submission_path: str):
        self.assignment_preprocessor = AssignmentPreProcessor(assignment_path)
        self.submission_preprocessor = SubmissionPreProcessor(submission_path)

    def run(self):
        print(self.assignment_preprocessor.run())
        print(self.submission_preprocessor.run())
