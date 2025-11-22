import sys
import argparse
from pathlib import Path

from src.autograder_ai.engine import Engine


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Autograder tool: provide assignment PDF and student submission."
    )

    parser.add_argument(
        "--assignment",
        required=True,
        type=Path,
        help="Path to the assignment PDF file.",
    )

    parser.add_argument(
        "--submission",
        required=True,
        type=Path,
        help="Path to the student's code submission file or directory.",
    )

    return parser.parse_args()


def validate_paths(assignment: Path, submission: Path):
    """Check if provided files/folders exist."""
    if not assignment.exists():
        print(f"Assignment file not found: {assignment}")
        sys.exit(1)

    if not submission.exists():
        print(f"Submission path not found: {submission}")
        sys.exit(1)


def main():
    args = parse_args()
    validate_paths(args.assignment, args.submission)
    engine = Engine(args.assignment, args.submission)
    engine.run()


if __name__ == "__main__":
    main()
