---
title: Testing
description: Learn how to test the Unraid API and its components
---

# Testing the Unraid API

This guide outlines the testing strategy and provides instructions for running various tests for the Unraid API project.

## Testing Philosophy

The Unraid API project follows a comprehensive testing approach, including:

- **Unit Tests**: Testing individual components in isolation
- **Integration Tests**: Testing interactions between components
- **End-to-End Tests**: Testing the API from a user's perspective
- **Mock Tests**: Testing with simulated Unraid server responses

Our testing philosophy emphasizes:

- Test-driven development when appropriate
- High test coverage for critical paths
- Realistic test scenarios that mirror actual usage
- Fast and reliable test execution

## Test Structure

Tests are organized by type and component:

```
tests/
├── unit/               # Unit tests
│   ├── client/         # Client tests
│   ├── resources/      # Resource tests
│   └── utils/          # Utility tests
├── integration/        # Integration tests
│   ├── client/         # Client integration tests
│   └── resources/      # Resource integration tests
├── e2e/                # End-to-end tests
│   ├── cli/            # CLI tests
│   ├── client/         # Client e2e tests
│   └── resources/      # Resource e2e tests
├── fixtures/           # Test fixtures and mock data
└── conftest.py         # Pytest configuration
```

## Setting Up the Test Environment

### Prerequisites

- Python 3.7+
- pytest
- pytest-cov
- pytest-mock
- A running Unraid server (for certain integration and E2E tests)

### Installation

```bash
# Install development dependencies
pip install -e ".[dev]"

# Or install testing dependencies directly
pip install pytest pytest-cov pytest-mock
```

## Running Tests

### Running All Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=unraid_api
```

### Running Specific Test Types

```bash
# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run end-to-end tests only
pytest tests/e2e/
```

### Running Tests for Specific Components

```bash
# Run tests for client
pytest tests/unit/client/ tests/integration/client/

# Run tests for a specific resource
pytest tests/unit/resources/test_array.py
```

## Mock Testing

For development and CI environments where a real Unraid server may not be available, we provide mock test capabilities.

### Using Mock Server

```bash
# Run tests with mock server
pytest --mock-server

# Run specific tests with mock server
pytest tests/integration/client/ --mock-server
```

### Creating Test Fixtures

Test fixtures are located in the `tests/fixtures` directory. To add new fixtures:

1. Create a JSON file with sample response data
2. Register the fixture in `conftest.py` if needed
3. Use the fixture in your tests

Example fixture usage:

```python
def test_get_array_info(mock_client, array_info_fixture):
    # Configure mock to return the fixture data
    mock_client.configure_mock("array/info", array_info_fixture)
    
    # Test the client with the fixture
    result = mock_client.array.info()
    assert result["status"] == "normal"
```

## Writing Tests

### Unit Test Example

```python
import pytest
from unraid_api.client import UnraidClient
from unraid_api.exceptions import AuthenticationError

def test_client_authentication_failure(monkeypatch):
    # Setup
    client = UnraidClient("http://example.com", "invalid_token")
    
    # Test authentication failure
    with pytest.raises(AuthenticationError):
        client.array.info()
```

### Integration Test Example

```python
def test_array_operations(unraid_client):
    # Get array status
    array_info = unraid_client.array.info()
    assert "status" in array_info
    
    # Test array operation (if array is stopped)
    if array_info["status"] == "stopped":
        result = unraid_client.array.start()
        assert result["success"] is True
```

### End-to-End Test Example

```python
def test_cli_array_info(cli_runner):
    # Run CLI command
    result = cli_runner.invoke(["array", "info"])
    
    # Verify output
    assert result.exit_code == 0
    assert "status" in result.json
```

## Continuous Integration

The Unraid API project uses GitHub Actions for continuous integration testing:

- Tests run on pull requests and pushes to main branch
- Tests run on multiple Python versions (3.7, 3.8, 3.9, 3.10)
- Coverage reports are generated and tracked

### CI Workflow

The CI workflow includes:

1. Setting up Python environment
2. Installing dependencies
3. Running linting (flake8, black)
4. Running unit tests
5. Running integration tests with mock server
6. Generating coverage report

## Test Coverage

We aim for high test coverage, especially for critical components:

- Client authentication and connection logic
- Resource operations
- Error handling
- CLI commands

Coverage reports are generated with pytest-cov:

```bash
# Generate HTML coverage report
pytest --cov=unraid_api --cov-report=html

# Open the HTML report
open htmlcov/index.html
```

## Mocking Strategies

### Server Response Mocking

```python
def test_with_mocked_response(mocker):
    # Mock the requests session
    mock_session = mocker.patch("unraid_api.client.requests.Session")
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {"status": "success", "data": {...}}
    mock_response.status_code = 200
    mock_session.return_value.get.return_value = mock_response
    
    # Test with mocked response
    client = UnraidClient("http://example.com", "token")
    result = client.array.info()
    assert result["status"] == "success"
```

### Environment Mocking

```python
def test_with_environment_variables(monkeypatch):
    # Set environment variables
    monkeypatch.setenv("UNRAID_URL", "http://example.com")
    monkeypatch.setenv("UNRAID_TOKEN", "test_token")
    
    # Test client initialization from environment
    client = UnraidClient.from_env()
    assert client.base_url == "http://example.com"
```

## Testing Best Practices

1. **Isolate Tests**: Each test should be independent and not rely on the state from other tests.

2. **Use Fixtures**: Utilize pytest fixtures for common setup and teardown operations.

3. **Mock External Dependencies**: Avoid making actual network requests in unit tests.

4. **Test Error Cases**: Ensure error handling works correctly by testing failure scenarios.

5. **Test Edge Cases**: Include tests for boundary conditions and uncommon scenarios.

6. **Keep Tests Fast**: Tests should execute quickly to encourage frequent running.

7. **Use Meaningful Assertions**: Make assertions specific and descriptive.

## Troubleshooting Tests

### Common Issues

- **Connection Failures**: Ensure the Unraid server is accessible for integration tests.
- **Authentication Issues**: Verify the API token is valid.
- **Timeouts**: Increase timeout settings for slower operations.
- **State Dependencies**: Reset state between tests if necessary.

### Debugging Tips

```bash
# Run with verbose output
pytest -v

# Run with debug logging
pytest --log-cli-level=DEBUG

# Run a specific test with focus
pytest tests/unit/test_specific.py::test_function -v
```

## Adding New Tests

When adding new features to the Unraid API, follow these steps:

1. Create corresponding test files in the appropriate test directory
2. Write tests before or alongside the implementation (TDD approach)
3. Ensure tests cover both success and failure scenarios
4. Add necessary fixtures for the new functionality
5. Update documentation if testing strategy changes

## Performance Testing

For resource-intensive operations, we include performance tests:

```python
import time

def test_performance_of_large_operation(unraid_client):
    # Measure execution time
    start_time = time.time()
    result = unraid_client.perform_large_operation()
    execution_time = time.time() - start_time
    
    # Assert on performance expectations
    assert execution_time < 5.0  # Operation should complete in under 5 seconds
``` 