# PLAN.md

## Solution plan

**Issue:** [Add `has_tests` Boolean to Repo Analysis Output](https://github.com/ascherj/pathreview/issues/50)

### Understand
`GitHubTool._fetch_repo_metadata` builds a metadata dict that includes `has_readme` by making a secondary API call to the GitHub readme endpoint, but never checks for test infrastructure — so `has_tests` is absent from the tool's output entirely. Downstream consumers (the agent and `RepoAnalyzer`) therefore have no signal on whether a repo is tested. The fix is symmetric with how `has_readme` already works: add a `_has_tests` method to `GitHubTool` that probes the GitHub Contents API for common test indicators, and include the result in the metadata dict.

### Map
Files to touch:
- `agent/tools/github_tool.py` — add `_has_tests` method and wire it into `_fetch_repo_metadata`
- `tests/unit/test_github_tool.py` — already written as the reproduction; update to pass once the fix is in

Files to read but not change:
- `ingestion/parsers/repo_analyzer.py` — reference for which test indicators to check (`tests/`, `test/`, `pytest.ini`, `test_*.py`)
- `agent/tools/base.py` — `ToolResult` dataclass shape

### Plan
1. Add `_has_tests(self, username, repo_name) -> bool` to `GitHubTool` following the same pattern as `_has_readme`: use `httpx.head` against the GitHub Contents API to check for `tests/`, `test/`, and `pytest.ini`. Return `True` if any path returns 200.
2. Wire `has_tests` into the metadata dict in `_fetch_repo_metadata` alongside `has_readme`.
3. Run the failing tests to confirm they now pass: `pytest tests/unit/test_github_tool.py -v`
4. Run the full unit suite to confirm no regressions: `make test-unit`
5. Update the log line in `_fetch_repo_metadata` to include `has_tests` for observability.

### Inputs & outputs
- **Input:** `github_username` + `repo_name` strings passed to `execute()`
- **New API calls made:** up to 3 `HEAD` requests to `/repos/{user}/{repo}/contents/{tests,test,pytest.ini}`
- **Output change:** `ToolResult.data` gains a `has_tests: bool` field alongside the existing `has_readme: bool`

### Risks & unknowns
- **GitHub API rate limits:** `_has_tests` adds up to 3 extra HEAD requests per call. With an API token this is fine (5000 req/hr); unauthenticated use (60 req/hr) could be a concern for heavy usage. Mitigation: short-circuit on first match to reduce calls from 3 to 1 in the happy path.
- **Repos that use non-standard test layouts:** A project using `src/tests/` or a monorepo with tests nested deeper won't be detected. This is acceptable for a first pass — the issue only asks for the common cases.
- **`httpx.head` vs `httpx.get` on contents:** The GitHub Contents API returns 200 for both HEAD and GET on existing paths. HEAD is cheaper since it skips the body. Confirm this behavior holds for directory paths (not just files).

### Edge cases
- Repo has no test infrastructure → `has_tests: False`
- Repo uses `test/` (singular) instead of `tests/` → should still return `True`
- Repo has only `pytest.ini` with no test files → returns `True` (conservative; the file signals intent)
- GitHub returns a non-200/404 status on a contents check (e.g., 403 rate-limited) → `_has_tests` should catch and return `False` rather than raising, matching the behavior of `_has_readme`
- `api_token` is set → auth header must be forwarded in the new HEAD calls (same as `_has_readme`)
