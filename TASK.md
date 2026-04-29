# Task: LLM Response Caching

## Context

You're working on an internal bank chatbot. Employees ask questions, and the service uses an LLM to generate answers based on a Knowledge Base.

```
┌──────────┐     ┌──────────────────┐     ┌─────────────┐     ┌─────┐
│  Client  │────▶│  Semantic Search │────▶│  KB Chat    │────▶│ LLM │
│          │     │  (external)      │     │  (this repo)│     │     │
└──────────┘     └──────────────────┘     └─────────────┘     └─────┘
                        │                        │
                        │ topic                  │ answer
                        ▼                        ▼
                 "vacation"              "You have 28 days..."
```

**Problem:** Every request goes to LLM → expensive, slow (~2 sec), inefficient.

**Your task:** Add response caching with Redis.

---

## Test Environment

The repo uses `RandomLLMClient` instead of a real LLM:
- Returns random strings (to verify cache works: same request → same response = cache hit)
- Emulates 2 second latency
- Has `fail_rate` parameter for error simulation

---

## Requirements

### 1. Cache Implementation

| Requirement | Details |
|-------------|---------|
| Storage | Redis |
| TTL | 5 minutes |
| Cache key | Must include: `prompt`, `system_prompt`, `model` |
| What to cache | Only successful LLM responses |

### 2. Cache Invalidation

| Requirement | Details |
|-------------|---------|
| By topic | `POST /api/v1/cache/invalidate/{topic}` — invalidates all cache entries for a topic |
| Mapping | You need to track which cache keys belong to which topic |

### 3. Response Format

The existing `ChatResponse` already has a `cached: bool` field. Set it to `true` for cache hits.

### 4. Tests (if there is time left)

Write tests for:
- Cache hit (second identical request returns cached response)
- Cache miss (different request goes to LLM)
- Invalidation (after invalidation, request goes to LLM again)

---

## Commands

```bash
# Install dependencies
uv sync --all-groups

# Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# Run server
uv run uvicorn kb_chat:create_app --factory --reload

# Run tests
uv run pytest tests/ -v
```
--- 