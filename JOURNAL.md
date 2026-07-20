# Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/50

**Issue title:** Add `has_tests` Boolean to Repo Analysis Output

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The repo analysis feature currently doesn't detect whether a repository has any testing infrastructure, so reviewers have no quick signal on test coverage. The issue asks for a `has_tests` boolean field to be added to the analysis output by checking for common indicators like `tests/` or `test/` directories, a `pytest.ini` config file, or files matching the `test_*.py` pattern. The fix lives in `agent/tools/github_tool.py` and `agent/tools/repo_analyzer.py`, and success means the analysis response includes an accurate `has_tests` field.

**Branch name:** feat/50-has-tests-boolean

**Setup confirmation:** [ ] App runs locally at localhost:5173

**Cohort ledger:** N/A (Tech Fellow)

---

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/avnigirish/pathreview/commit/5731dce5a7c37eee665759267b6821940c56f005

**Reproduction summary:**
`GitHubTool._fetch_repo_metadata` returns a metadata dict that includes `has_readme` but not `has_tests` — the field simply doesn't exist in the output. I confirmed this by writing a failing unit test (`tests/unit/test_github_tool.py`) that asserts `has_tests` is present in `result.data`; it fails on the current code with a `KeyError`/assertion error, pinpointing exactly where the gap lives.

**PLAN.md link:** https://github.com/avnigirish/pathreview/blob/feat/50-has-tests-boolean/PLAN.md

**Walkthrough video (recommended):** N/A

**Blockers or open questions:**
Need to confirm that `httpx.head` works correctly against GitHub's Contents API for directory paths (not just files) — will verify during implementation.
