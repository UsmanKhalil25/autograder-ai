import time
import tempfile
from pathlib import Path
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langchain_community.tools import ShellTool
from langchain.agents import create_agent

from ..states import TestExecutionState, TestResult, EvaluationStatus
from ..prompts import TEST_EXECUTION_PROMPT
from ...utils import parse_agent_response


def _format_input_for_stdin(input_params: Dict[str, Any]) -> str:

    if len(input_params) == 1:
        return str(list(input_params.values())[0])

    return " ".join(str(v) for v in input_params.values())


def setup_code_file_node(state: TestExecutionState) -> TestExecutionState:
    print(f"  → Setting up code file for execution")

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, dir="/tmp", prefix="code_"
    ) as f:
        f.write(state["code"])
        temp_path = f.name

    state["code_file_path"] = temp_path
    state["status"] = EvaluationStatus.PROCESSING
    print(f"  ✓ Code written to: {temp_path}")

    return state


def initialize_execution_node(state: TestExecutionState) -> TestExecutionState:
    print(f"  → Initializing test execution for {state['question_id']}")

    state["current_test_index"] = 0
    state["test_results"] = []
    state["status"] = EvaluationStatus.PROCESSING

    print(f"  ✓ Found {len(state['test_cases'])} test cases to execute")

    return state


def should_continue_testing(state: TestExecutionState) -> str:
    if state["current_test_index"] < len(state["test_cases"]):
        return "execute_test"
    else:
        return "finalize"


def execute_single_test_node(llm):

    def node(state: TestExecutionState) -> TestExecutionState:
        """Node: Execute a single test case using agent"""

        test_idx = state["current_test_index"]
        test_case = state["test_cases"][test_idx]

        print(f"\n  → Executing Test {test_idx + 1}/{len(state['test_cases'])}")
        print(f"    Description: {test_case.get('description', 'N/A')}")

        stdin_input = _format_input_for_stdin(test_case["input"])

        shell_tool = ShellTool()
        agent = create_agent(model=llm, tools=[shell_tool])

        prompt = TEST_EXECUTION_PROMPT.format(
            code_file_path=state["code_file_path"],
            stdin_input=stdin_input,
            description=test_case.get("description", "No description"),
            input_params=test_case["input"],
            expected_output=test_case["expected_output"],
        )

        input_message = HumanMessage(content=prompt)

        start_time = time.time()
        actual_output = None
        reasoning = ""
        passed = False
        execution_error = None

        try:
            messages = []
            for step in agent.stream(
                {"messages": [input_message]}, stream_mode="values"
            ):
                messages.append(step["messages"][-1])

            last_message = messages[-1].content if messages else ""

            passed, actual_output, reasoning = parse_agent_response(last_message)

        except Exception as e:
            execution_error = str(e)
            reasoning = f"Execution failed with error: {execution_error}"
            passed = False
            actual_output = None
            print(f"    ✗ Error during execution: {e}")

        execution_time = time.time() - start_time

        test_result: TestResult = {
            "test_index": test_idx,
            "description": test_case.get("description", ""),
            "input": test_case["input"],
            "expected_output": test_case["expected_output"],
            "actual_output": actual_output,
            "passed": passed,
            "reasoning": reasoning,
            "execution_error": execution_error,
            "execution_time": execution_time,
        }

        state["test_results"].append(test_result)
        state["current_test_index"] += 1

        status_symbol = "✓" if passed else "✗"
        print(f"    {status_symbol} Test {'PASSED' if passed else 'FAILED'}")

        return state

    return node


def finalize_execution_node(state: TestExecutionState) -> TestExecutionState:
    print(f"\n  → Finalizing test execution")

    try:
        Path(state["code_file_path"]).unlink()
        print(f"  ✓ Cleaned up temporary file")
    except Exception as e:
        print(f"  ! Warning: Could not delete temporary file: {e}")

    total_tests = len(state["test_results"])
    passed_tests = sum(1 for result in state["test_results"] if result["passed"])

    state["status"] = EvaluationStatus.COMPLETED

    print(f"  ✓ Execution complete: {passed_tests}/{total_tests} tests passed")

    return state
