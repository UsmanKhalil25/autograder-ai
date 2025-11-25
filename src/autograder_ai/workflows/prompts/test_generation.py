TEST_GENERATION_PROMPT = """
You are an expert software tester.

Your goal is to generate a list of input dictionaries that simulate how real users
would interact with the given assignment problem.

These are NOT unit tests and NOT expected outputs.  
They are only **input variations** that will be fed into the student's code.

-----------------------------
ASSIGNMENT QUESTION
{question}

-----------------------------
SUBMITTED CODE
{code}

-----------------------------
REQUIREMENTS FOR THE TEST CASES

1. Produce **ONLY** a JSON list of dictionaries.  
   No explanation, no comments, no text outside JSON.

2. Each dictionary represents a single run of the program  
   and contains **only the input parameters** needed by the code.

3. You must infer which parameters are required by the program
   by analyzing the submitted code and the assignment question.

4. Include **all these categories** of cases:
   - Typical / normal inputs
   - Boundary inputs
   - Edge cases
   - Invalid or unexpected inputs (but still syntactically correct)
   - Stress / large-value cases (if relevant)

5. Generate **8–15 test cases**, depending on complexity.

6. Every test case must be a **pure dictionary of primitive types** (str, int, float, bool, list).

7. Do not wrap the list in any outer structure.  
   Output must be directly assignable to `test_cases: List[Dict[str, Any]]`.

-----------------------------
OUTPUT FORMAT (IMPORTANT)

[
  {"input_param1": value, "input_param2": value},
  {"input_param1": value, "input_param2": value}
]

Only valid JSON. No trailing commas. No comments.

Now generate the test case list.
"""

