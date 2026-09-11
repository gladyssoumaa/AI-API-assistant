from __future__ import annotations

import time

import httpx


def flatten_tests(tests: dict) -> list[dict]:
    flattened = []

    for category in [
        "positive",
        "negative",
        "boundary",
        "edge",
        "security",
    ]:
        category_tests = tests.get(category, [])

        if not isinstance(category_tests, list):
            continue

        for test in category_tests:
            if isinstance(test, dict):
                test["category"] = category
                flattened.append(test)

    return flattened


def run_api_tests(
    base_url: str,
    tests: dict,
) -> list[dict]:
    results = []
    flattened_tests = flatten_tests(tests)

    with httpx.Client(
        base_url=base_url.rstrip("/"),
        timeout=10.0,
    ) as client:

        for test in flattened_tests:
            start = time.perf_counter()

            try:
                response = client.request(
                    method=test["method"],
                    url=test["path"],
                    headers=test.get("headers") or {},
                    params=test.get("query_params") or {},
                    json=test.get("request_body"),
                )

                elapsed = (
                    time.perf_counter() - start
                ) * 1000

                results.append(
                    {
                        "name": test["name"],
                        "category": test.get(
                            "category",
                            "unknown",
                        ),
                        "method": test["method"],
                        "path": test["path"],
                        "expected_status_code": test[
                            "expected_status_code"
                        ],
                        "actual_status_code": response.status_code,
                        "passed": (
                            response.status_code
                            == test["expected_status_code"]
                        ),
                        "response_time_ms": round(
                            elapsed,
                            2,
                        ),
                        "error": None,
                    }
                )

            except Exception as exc:
                elapsed = (
                    time.perf_counter() - start
                ) * 1000

                results.append(
                    {
                        "name": test["name"],
                        "category": test.get(
                            "category",
                            "unknown",
                        ),
                        "method": test["method"],
                        "path": test["path"],
                        "expected_status_code": test[
                            "expected_status_code"
                        ],
                        "actual_status_code": None,
                        "passed": False,
                        "response_time_ms": round(
                            elapsed,
                            2,
                        ),
                        "error": str(exc),
                    }
                )

    return results