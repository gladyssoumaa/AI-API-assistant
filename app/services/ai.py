from __future__ import annotations

import json

from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL


if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not configured.")


client = Groq(api_key=GROQ_API_KEY)


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

    elif content.startswith("```"):
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
You are an expert API documentation, testing, and security assistant.

Analyze this API endpoint.

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

documentation must contain clear and practical API documentation.

request_example must contain a realistic example request.

response_example must contain a realistic example response.

test_cases must be an array of useful API test cases.

Each test case must contain:

name
category
method
path
headers
query_params
request_body
expected_status_code
expected_behavior

The category must be one of:

positive
negative
boundary
edge
security

Generate tests across all five categories.

Positive tests must verify valid expected behavior.

Negative tests must verify invalid input, missing required fields, incorrect types, invalid values, and invalid requests where applicable.

Boundary tests must verify minimum, maximum, zero, length, size, numeric, date, or other meaningful limits based on the actual endpoint fields.

Edge tests must verify unusual but realistic situations such as empty values, null optional values, special characters, duplicate requests, unusual combinations, or other endpoint-specific edge conditions.

Security tests must verify relevant authentication, authorization, access control, injection, malformed tokens, IDOR, sensitive data exposure, input validation, and other realistic security risks.

Do not generate irrelevant tests for fields or functionality that do not exist.

Each category must contain at least 3 tests.

security tests must contain at least 4 tests when the endpoint supports authentication or authorization.

request_body must be a JSON object when the endpoint accepts a body, otherwise null.

headers must be a JSON object.

query_params must be a JSON object.

expected_status_code must be an integer.

security_recommendations must be an array.

Keep the response concise.

Do not use markdown.

Return JSON only.
"""

    result = call_ai(
        prompt,
        "You are a professional API documentation, testing, and security assistant. Return valid JSON only.",
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

project_overview must be a concise description of the API project.

documentation must be an array of important documentation improvements.

test_strategy must be an array of recommended testing strategies.

security_recommendations must be an array of practical security recommendations.

issues_found must be an array of important problems, inconsistencies, missing information, or risks.

Consider:

API consistency
HTTP methods
status codes
request validation
response structures
authentication
authorization
input validation
error handling
security
testing coverage
documentation completeness

Keep every field concise.

Do not use markdown.

Return JSON only.
"""

    result = call_ai(
        prompt,
        "You are a professional API documentation, testing, and security assistant. Return valid JSON only.",
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
) -> dict:
    prompt = f"""
You are an expert API test engineer and application security tester.

Generate a comprehensive test suite for this API endpoint.

HTTP method: {method}
Path: {path}
Summary: {summary}
Description: {description}
Request body: {request_body}
Response body: {response_body}
Expected response status code: {response_status_code}

Return valid JSON with exactly these fields:

positive
negative
boundary
edge
security

Each field must contain an array of test cases.

Every test case must contain exactly these fields:

name
category
method
path
headers
query_params
request_body
expected_status_code
expected_behavior

category must match the parent category.

Generate at least:

3 positive tests
3 negative tests
3 boundary tests
3 edge tests
4 security tests when security testing is applicable

Positive tests:
Test valid requests and successful expected behavior.

Negative tests:
Test missing required fields, invalid fields, invalid types, invalid enum values, malformed identifiers, invalid requests, and expected validation failures.

Boundary tests:
Test meaningful minimum and maximum values, zero values, string length limits, numeric limits, date boundaries, pagination limits, and other limits that actually apply to this endpoint.

Edge tests:
Test empty values, null optional fields, special characters, duplicate requests, unusual valid combinations, large but reasonable payloads, and other realistic edge conditions.

Security tests:
Test missing authentication, invalid authentication, expired or malformed tokens, authorization failures, IDOR, injection attempts, sensitive data exposure, privilege escalation, and input-based attacks where relevant.

Do not generate irrelevant tests.

Do not invent fields that do not exist.

Do not assume a maximum or minimum value unless it can reasonably be inferred from the endpoint definition.

If authentication is not indicated, security tests should focus on input validation, injection, access control assumptions, and other applicable security risks.

headers must be a JSON object.

query_params must be a JSON object.

request_body must be a JSON object when the endpoint accepts a body, otherwise null.

expected_status_code must be an integer.

expected_behavior must clearly explain what the API should do.

Return JSON only.
"""

    result = call_ai(
        prompt,
        "You are an expert API test engineer and application security tester. Generate comprehensive, realistic, endpoint-specific tests. Return valid JSON only.",
    )

    required_categories = [
        "positive",
        "negative",
        "boundary",
        "edge",
        "security",
    ]

    for category in required_categories:
        if category not in result:
            raise RuntimeError(
                f"AI response is missing test category: {category}"
            )

        if not isinstance(result[category], list):
            raise RuntimeError(
                f"Test category '{category}' must be an array."
            )

    return result


def analyze_test_failures(
    endpoint: dict,
    test_results: list[dict],
) -> dict:
    prompt = f"""
You are an expert API debugging and security assistant.

Analyze the following endpoint and its test results.

Endpoint:

{json.dumps(endpoint, indent=2)}

Test results:

{json.dumps(test_results, indent=2)}

Return valid JSON with exactly these fields:

summary
root_causes
recommendations
security_concerns

summary must be a concise explanation of the overall test outcome.

root_causes must be an array of likely causes for failed tests.

recommendations must be an array of practical fixes.

security_concerns must be an array of security issues revealed by the failures.

Do not invent information that is not supported by the endpoint or test results.

Return JSON only.
"""

    result = call_ai(
        prompt,
        "You are an expert API debugging and security assistant. Return valid JSON only.",
    )

    required_fields = [
        "summary",
        "root_causes",
        "recommendations",
        "security_concerns",
    ]

    for field in required_fields:
        if field not in result:
            raise RuntimeError(
                f"AI response is missing required field: {field}"
            )

    return result