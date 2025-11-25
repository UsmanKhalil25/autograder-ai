import json

from ..states import TestGenerationState
from ..prompts import TEST_GENERATION_PROMPT
from ...utils import extract_json


def analyze_question_node(state: TestGenerationState) -> TestGenerationState:
    """Node: Analyze the assignment question"""
    print(f"  → Analyzing question: {state['question_id']}")
    return state


def analyze_code_node(state: TestGenerationState) -> TestGenerationState:
    """Node: Analyze the submitted code"""
    print(f"  → Analyzing submitted code")
    return state

def generate_test_cases_node(llm):
    def node(state):
        prompt = TEST_GENERATION_PROMPT.format(
            question=state["question"],
            code=state["code"]
        )

        response = llm.invoke(prompt)
        content = response.content

        # Extract JSON from the response
        json_str = extract_json(content)

        try:
            state["test_cases"] = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"  ✗ Failed to parse JSON: {e}")
            print(f"  Response content: {content[:200]}...")
            state["test_cases"] = []

        return state

    return node

def validate_tests_node(state: TestGenerationState) -> TestGenerationState:

    raw_cases = state.get("test_cases", None)

    if not isinstance(raw_cases, list):
        print("LLM returned a non-list -- resetting test_cases to empty list")
        state["test_cases"] = []
        return state

    validated = []

    for index, case in enumerate(raw_cases):
        if not isinstance(case, dict):
            print(f"Test case {index} is not a dict. Skipping.")
            continue

        cleaned_case = {}

        for key, value in case.items():

            if not isinstance(key, str):
                print(f"Invalid key type in case {index}: {key} (ignored)")
                continue

            if isinstance(value, (str, int, float, bool)) or value is None:
                cleaned_case[key] = value

            elif isinstance(value, list):
                if all(isinstance(x, (str, int, float, bool, type(None))) for x in value):
                    cleaned_case[key] = value
                else:
                    print(f"List contains invalid types in case {index}, key '{key}'")
            else:
                print(f"Unsupported value type in case {index}, key '{key}': {type(value)}")

        if cleaned_case:
            validated.append(cleaned_case)

    state["test_cases"] = validated
    return state

