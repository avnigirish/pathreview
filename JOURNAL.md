# Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/83

**Issue title:** Add a `GET /health` endpoint with dependency status checks

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
PathReview currently has no health check endpoint, making it impossible for infrastructure monitoring tools to verify that the service and its dependencies are up. The issue asks for a `GET /health` route (in `api/routes/health.py`) that checks the status of each backing service — PostgreSQL, Redis, and the ChromaDB vector store — and returns a structured response indicating which dependencies are healthy or degraded. A successful fix means operators can point an uptime monitor or load-balancer health probe at this endpoint and get actionable status information.

**Branch name:** feat/83-health-endpoint

**Setup confirmation:** [ ] App runs locally at localhost:5173

**Cohort ledger:** N/A (Tech Fellow)
