"""Tests for github_tool.py

Reproduction of issue #50: GitHubTool.execute() returns metadata that includes
has_readme but is missing has_tests, so downstream consumers have no signal on
whether the repo contains testing infrastructure.
"""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from agent.tools.github_tool import GitHubTool

MOCK_REPO_RESPONSE: dict[str, Any] = {
    "name": "my-project",
    "description": "A sample project",
    "language": "Python",
    "stargazers_count": 10,
    "forks_count": 2,
    "open_issues_count": 1,
    "pushed_at": "2024-01-01T00:00:00Z",
    "topics": ["python", "fastapi"],
    "homepage": "https://example.com",
}


def _make_mock_response(json_data: dict[str, Any], status_code: int = 200) -> MagicMock:
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    mock.raise_for_status = MagicMock()
    return mock


@pytest.mark.unit
class TestGitHubTool:
    """Test suite for GitHubTool."""

    @pytest.fixture
    def tool(self) -> GitHubTool:
        return GitHubTool()

    @patch("agent.tools.github_tool.httpx.get")
    @patch("agent.tools.github_tool.httpx.head")
    def test_result_includes_has_tests_field(
        self, mock_head: MagicMock, mock_get: MagicMock, tool: GitHubTool
    ) -> None:
        """Reproduction of issue #50: has_tests must be present in result data.

        This test FAILS on the current implementation because _fetch_repo_metadata
        never checks for test infrastructure and never sets has_tests in its output.
        """
        mock_get.return_value = _make_mock_response(MOCK_REPO_RESPONSE)
        mock_head.return_value = _make_mock_response({}, status_code=200)

        result = tool.execute({"github_username": "testuser", "repo_name": "my-project"})

        assert result.success is True
        # FAILS: 'has_tests' not in result.data — this is the gap being fixed
        assert "has_tests" in result.data, "has_tests missing from GitHubTool output (issue #50)"

    @patch("agent.tools.github_tool.httpx.get")
    @patch("agent.tools.github_tool.httpx.head")
    def test_has_tests_true_when_tests_dir_exists(
        self, mock_head: MagicMock, mock_get: MagicMock, tool: GitHubTool
    ) -> None:
        """has_tests should be True when the repo has a tests/ directory."""
        mock_get.return_value = _make_mock_response(MOCK_REPO_RESPONSE)

        def head_side_effect(url: str, **kwargs: Any) -> MagicMock:
            if "/contents/tests" in url or "/readme" in url:
                return _make_mock_response({}, status_code=200)
            return _make_mock_response({}, status_code=404)

        mock_head.side_effect = head_side_effect

        result = tool.execute({"github_username": "testuser", "repo_name": "my-project"})

        assert result.success is True
        assert result.data.get("has_tests") is True

    @patch("agent.tools.github_tool.httpx.get")
    @patch("agent.tools.github_tool.httpx.head")
    def test_has_tests_false_when_no_test_infrastructure(
        self, mock_head: MagicMock, mock_get: MagicMock, tool: GitHubTool
    ) -> None:
        """has_tests should be False when the repo has no test files or dirs."""
        mock_get.return_value = _make_mock_response(MOCK_REPO_RESPONSE)

        def head_side_effect(url: str, **kwargs: Any) -> MagicMock:
            if "/readme" in url:
                return _make_mock_response({}, status_code=200)
            return _make_mock_response({}, status_code=404)

        mock_head.side_effect = head_side_effect

        result = tool.execute({"github_username": "testuser", "repo_name": "my-project"})

        assert result.success is True
        assert result.data.get("has_tests") is False

    @patch("agent.tools.github_tool.httpx.get")
    @patch("agent.tools.github_tool.httpx.head")
    def test_result_has_all_required_fields(
        self, mock_head: MagicMock, mock_get: MagicMock, tool: GitHubTool
    ) -> None:
        """Result data should include both has_readme and has_tests."""
        mock_get.return_value = _make_mock_response(MOCK_REPO_RESPONSE)
        mock_head.return_value = _make_mock_response({}, status_code=200)

        result = tool.execute({"github_username": "testuser", "repo_name": "my-project"})

        assert result.success is True
        for field in ("name", "primary_language", "star_count", "has_readme", "has_tests"):
            assert field in result.data, f"Missing field: {field}"
