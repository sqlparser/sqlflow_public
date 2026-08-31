"""Shared pytest fixtures and configuration."""

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator, Dict, Any
from unittest.mock import Mock, MagicMock

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_sql_query() -> str:
    """Provide a sample SQL query for testing."""
    return """
    SELECT 
        u.user_id,
        u.username,
        COUNT(o.order_id) as order_count,
        SUM(o.total_amount) as total_spent
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id
    WHERE u.created_at >= '2023-01-01'
    GROUP BY u.user_id, u.username
    HAVING COUNT(o.order_id) > 0
    ORDER BY total_spent DESC
    LIMIT 100;
    """


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Provide a mock configuration dictionary."""
    return {
        "api": {
            "base_url": "https://api.example.com",
            "timeout": 30,
            "retry_count": 3,
            "api_key": "test-api-key"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "test_db",
            "user": "test_user",
            "password": "test_password"
        },
        "logging": {
            "level": "DEBUG",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }


@pytest.fixture
def config_file(temp_dir: Path, mock_config: Dict[str, Any]) -> Path:
    """Create a temporary config file with mock configuration."""
    config_path = temp_dir / "config.json"
    with open(config_path, 'w') as f:
        json.dump(mock_config, f, indent=2)
    return config_path


@pytest.fixture
def mock_http_client() -> Mock:
    """Create a mock HTTP client for API testing."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {"result": "mocked"}
    }
    mock_response.text = '{"status": "success", "data": {"result": "mocked"}}'
    mock_client.get.return_value = mock_response
    mock_client.post.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_database_connection() -> Mock:
    """Create a mock database connection."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = [
        (1, "user1", 5, 1500.00),
        (2, "user2", 3, 750.50)
    ]
    mock_cursor.fetchone.return_value = (1, "user1", 5, 1500.00)
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn


@pytest.fixture
def sample_api_response() -> Dict[str, Any]:
    """Provide a sample API response for testing."""
    return {
        "status": "success",
        "code": 200,
        "data": {
            "lineage": {
                "tables": [
                    {"name": "users", "type": "source"},
                    {"name": "orders", "type": "source"}
                ],
                "columns": [
                    {"table": "users", "column": "user_id", "dataflow": "direct"},
                    {"table": "orders", "column": "order_id", "dataflow": "aggregate"}
                ]
            },
            "metadata": {
                "query_id": "12345",
                "execution_time": 0.156,
                "rows_affected": 100
            }
        }
    }


@pytest.fixture
def sql_file(temp_dir: Path, sample_sql_query: str) -> Path:
    """Create a temporary SQL file."""
    sql_path = temp_dir / "test_query.sql"
    with open(sql_path, 'w') as f:
        f.write(sample_sql_query)
    return sql_path


@pytest.fixture
def mock_env_vars(monkeypatch) -> Dict[str, str]:
    """Set up mock environment variables."""
    env_vars = {
        "SQLFLOW_API_KEY": "test-api-key",
        "SQLFLOW_BASE_URL": "https://api.test.sqlflow.com",
        "SQLFLOW_TIMEOUT": "60",
        "DATABASE_URL": "postgresql://test:test@localhost:5432/testdb"
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


@pytest.fixture
def mock_file_system(temp_dir: Path) -> Dict[str, Path]:
    """Create a mock file system structure for testing."""
    structure = {
        "input": temp_dir / "input",
        "output": temp_dir / "output",
        "logs": temp_dir / "logs",
        "cache": temp_dir / "cache"
    }
    
    for directory in structure.values():
        directory.mkdir(parents=True, exist_ok=True)
    
    # Create some sample files
    (structure["input"] / "sample.sql").write_text("SELECT * FROM users;")
    (structure["input"] / "config.json").write_text('{"key": "value"}')
    
    return structure


@pytest.fixture(autouse=True)
def cleanup_test_files(request):
    """Automatically clean up any test files created during tests."""
    yield
    # Cleanup logic can be added here if needed
    pass


@pytest.fixture
def mock_logger() -> Mock:
    """Create a mock logger for testing logging functionality."""
    mock_log = Mock()
    mock_log.debug = Mock()
    mock_log.info = Mock()
    mock_log.warning = Mock()
    mock_log.error = Mock()
    mock_log.critical = Mock()
    return mock_log


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (may require external resources)"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )