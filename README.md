# AI-API-assistant

# AI API Documentation & Testing Assistant

An AI-powered backend system for automatically analyzing API endpoints, generating API documentation, creating comprehensive test cases, executing API tests, and identifying security risks.

## Overview

The AI API Documentation & Testing Assistant helps developers understand, document, test, and improve APIs without manually creating every piece of documentation and test case.

The system allows users to:

- Create and manage API projects
- Register API endpoints
- Analyze endpoints using artificial intelligence
- Generate API documentation
- Generate realistic request and response examples
- Generate categorized API test cases
- Execute generated tests against an API
- Store and review test results
- Analyze project-wide API quality
- Identify potential security concerns
- Generate security recommendations
- Manage authenticated users
- Apply role-based access control
- Provide administrative statistics

The backend exposes a REST API through FastAPI and provides interactive API documentation through Swagger/OpenAPI.

## Key Features

### Authentication

The system provides secure user authentication using:

- JWT access tokens
- Password hashing
- OAuth2 password authentication
- Protected API endpoints
- User roles

Users are assigned roles such as:

- `user`
- `admin`

Administrative endpoints are protected and can only be accessed by administrators.

### API Project Management

Authenticated users can create and manage API projects.

Each project contains:

- Project name
- Description
- Base URL
- Owner
- API endpoints

Projects are isolated between users so that users can only access their own projects.

### Endpoint Management

Users can register API endpoints containing information such as:

- HTTP method
- Path
- Summary
- Description
- Request body
- Response body
- Expected response status code

This information is used by the AI system to understand and analyze each endpoint.

### AI Endpoint Analysis

The system uses the Groq API to analyze individual API endpoints.

The AI generates:

- API documentation
- Request examples
- Response examples
- Test cases
- Security recommendations

The generated information is stored in PostgreSQL for later retrieval.

### AI Test Generation

The system generates endpoint-specific tests in five categories:

1. Positive tests
2. Negative tests
3. Boundary tests
4. Edge tests
5. Security tests

The generated tests consider the endpoint's method, path, request body, response structure, expected status code, validation requirements, authentication requirements, and security risks.

### Automated API Test Execution

Generated tests can be executed automatically against the configured API base URL.

The test runner records:

- Test name
- Test category
- HTTP method
- Request path
- Expected status code
- Actual status code
- Pass/fail status
- Response time
- Error information

Test results are stored in PostgreSQL.

### Project-Level AI Analysis

The system can analyze all endpoints within a project and provide:

- Project overview
- Documentation improvements
- Testing strategies
- Security recommendations
- Potential API issues

### Security Analysis

The AI considers common API security concerns including:

- Authentication failures
- Authorization failures
- Invalid tokens
- Expired tokens
- IDOR vulnerabilities
- Input validation problems
- Injection attacks
- Sensitive information exposure
- Privilege escalation
- Improper error handling

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT
- OAuth2
- Alembic
- HTTPX

### Artificial Intelligence

- Groq API
- Large Language Model based API analysis
- AI-generated documentation
- AI-generated test cases
- AI-assisted security analysis

### Testing

- Pytest
- HTTPX
- Automated API test execution

### API Documentation

- OpenAPI
- Swagger UI
- FastAPI documentation

## System Architecture

```text
                    ┌──────────────────────┐
                    │      Frontend        │
                    │  Developer Dashboard │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │      REST API        │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │     Auth    │   │   Projects  │   │  Endpoints  │
      │    & RBAC   │   │ Management  │   │ Management  │
      └─────────────┘   └─────────────┘   └──────┬──────┘
                                                 │
                                                 ▼
                                      ┌────────────────────┐
                                      │    AI Analysis     │
                                      │       Service      │
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │      Groq API      │
                                      │        LLM         │
                                      └────────────────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │    Test Runner     │
                                      │       HTTPX        │
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │     PostgreSQL     │
                                      │      Database      │
                                      └────────────────────┘