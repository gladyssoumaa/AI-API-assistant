from __future__ import annotations
import json
from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not configured.")


client = Groq(
    api_key=GROQ_API_KEY,
)


def call_ai(prompt: str, system_message: str) -> dict:
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=4096,
        )
    except Exception as exc:
        raise RuntimeError(
            f"Groq API request failed: {type(exc).__name__}: {exc}"
        ) from exc

    if not response.choices:
        raise RuntimeError("Groq returned no choices.")

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Groq returned an empty response.")

    content = content.strip()

    if content.startswith("```json"):
        content = content[7:]

    if content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    try:
        result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Groq returned invalid JSON: {content}"
        ) from exc

    if not isinstance(result, dict):
        raise RuntimeError("Groq response is not a JSON object.")

    return result


def analyze_project(endpoints: list[dict]) -> dict:
    prompt = f"""
You are an expert API documentation, testing, and security assistant.

Analyze this API project:

{json.dumps(endpoints, indent=2)}

Return valid JSON with exactly these fields:

project_overview
documentation
test_strategy
security_recommendations
issues_found

project_overview must be a concise paragraph.

documentation must be a concise list of the most important API documentation improvements.

test_strategy must be an array of recommended tests.

security_recommendations must be an array of practical security recommendations.

issues_found must be an array of important problems, inconsistencies, missing information, or risks.

Keep every field concise.

Do not use markdown.

Return JSON only.
"""

    result = call_ai(
        prompt,
        "You are a professional API documentation, testing, and security assistant. Return concise valid JSON only.",
    )

    required_fields = [
        "project_overview",
        "documentation",
        "test_strategy",
        "security_recommendations",
        "issues_found",
    ]

    for field in required_fields:
        if field not in result:
            raise RuntimeError(
                f"AI response is missing required field: {field}"
            )

    return result



def analyze_project(endpoints: list[dict]) -> dict:
    prompt = f"""
You are an expert API documentation, testing, and security assistant.

Analyze the following API project:

{json.dumps(endpoints, indent=2)}

Return valid JSON with exactly these fields:

project_overview
documentation
test_strategy
security_recommendations
issues_found

project_overview must provide a concise overview of the API.

documentation must provide useful documentation guidance for the API as a whole.

test_strategy must be an array of recommended tests.

security_recommendations must be an array of security recommendations.

issues_found must be an array of problems, inconsistencies, missing information, or risks you identify.

Return JSON only.
"""

    result = call_ai(
        prompt,
        "You are a professional API documentation, testing, and security assistant.",
    )

    required_fields = [
        "project_overview",
        "documentation",
        "test_strategy",
        "security_recommendations",
        "issues_found",
    ]

    for field in required_fields:
        if field not in result:
            raise RuntimeError(
                f"AI response is missing required field: {field}"
            )

    return result

def generate_tests(
    method: str,
    path: str,
    summary: str | None,
    description: str | None,
    request_body: str | None,
    response_body: str | None,
    response_status_code: int | None,
) -> list[dict]:
    prompt = f"""
You are an API testing expert.

Generate useful automated test cases for this API endpoint.

HTTP method: {method}
Path: {path}
Summary: {summary}
Description: {description}
Request body: {request_body}
Response body: {response_body}
Expected response status code: {response_status_code}

Generate tests covering:

1. Successful request
2. Invalid input
3. Missing required data
4. Authentication or authorization where relevant
5. Invalid resource or parameters where relevant
6. Edge cases

Return valid JSON with exactly this field:

tests

tests must be an array.

Each test must contain exactly:

name
description
method
path
expected_status_code

Return JSON only.
"""

    result = call_ai(
        prompt,
        "You are an expert API testing assistant.",
    )

    if "tests" not in result:
        raise RuntimeError("AI response does not contain tests.")

    if not isinstance(result["tests"], list):
        raise RuntimeError("AI tests field is not an array.")

    return result["tests"]


def analyze_test_failures(
    endpoint: dict,
    results: list[dict],
) -> dict:
    prompt = f"""
You are an expert API debugging assistant.

Analyze the failed API tests below.

Endpoint:
{json.dumps(endpoint, indent=2)}

Test results:
{json.dumps(results, indent=2)}

Return valid JSON with exactly these fields:

summary
failures
recommendations

summary must explain the overall test result.

failures must be an array explaining each important failure.

recommendations must be an array containing practical recommendations for fixing the failures.

Return JSON only.
"""

    result = call_ai(
        prompt,
        "You are an expert API debugging assistant.",
    )

    required_fields = [
        "summary",
        "failures",
        "recommendations",
    ]

    for field in required_fields:
        if field not in result:
            raise RuntimeError(
                f"AI response is missing required field: {field}"
            )

    return result

def analyze_endpoint(
    method: str,
    path: str,
    summary: str | None,
    description: str | None,
    request_body: str | None,
    response_body: str | None,
    response_status_code: int | None,
) -> dict:
    prompt = f"""
You are an API documentation and testing assistant.

Analyze the following API endpoint.

HTTP method: {method}
Path: {path}
Summary: {summary}
Description: {description}
Request body: {request_body}
Response body: {response_body}
Expected response status code: {response_status_code}

Return valid JSON with exactly these fields:

documentation
request_example
response_example
test_cases
security_recommendations

documentation must contain clear API documentation.

request_example must contain a realistic example request.

response_example must contain a realistic example response.

test_cases must be an array of useful API test cases.

security_recommendations must be an array of security recommendations relevant to this endpoint.

Keep the response concise.

Return JSON only.
"""

    result = call_ai(
        prompt,
        "You are a professional API documentation, testing, and security assistant. Return concise valid JSON only.",
    )

    required_fields = [
        "documentation",
        "request_example",
        "response_example",
        "test_cases",
        "security_recommendations",
    ]

    for field in required_fields:
        if field not in result:
            raise RuntimeError(
                f"AI response is missing required field: {field}"
            )

    return result