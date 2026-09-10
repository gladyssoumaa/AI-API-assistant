from __future__ import annotations
import time
import httpx


def run_api_tests(
    base_url: str,
    tests: list[dict],
) -> list[dict]:
    results = []

    with httpx.Client(
        base_url=base_url,
        timeout=10.0,
    ) as client:
        for test in tests:
            start = time.perf_counter()

            try:
                response = client.request(
                    method=test["method"],
                    url=test["path"],
                )

                elapsed = (
                    time.perf_counter() - start
                ) * 1000

                results.append(
                    {
                        "name": test["name"],
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