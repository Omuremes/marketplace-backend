
# Key Prompts and AI Interaction Rules

This document records representative prompts used to guide AI development.

The goal was consistency and architectural control rather than ad-hoc generation.

---

## Global Prompt Rules

All prompts followed constraints:

* async Python only
* clean architecture separation
* FastAPI routers must remain thin
* repositories abstract ORM
* domain layer framework-independent
* production-oriented structure

---

## Backend Architecture Prompt

```
Design a FastAPI backend using clean architecture principles.

Constraints:
- async SQLAlchemy 2.x
- repository pattern
- service layer owns business logic
- routers contain no business logic
- domain must not depend on FastAPI or ORM
- include Unit of Work pattern
```

---

## Repository Generation Prompt

```
Implement repository methods for Product entity.

Requirements:
- async queries
- cursor pagination support
- return domain entities, not ORM models
- avoid N+1 queries
```

---

## Pagination Optimization Prompt

```
Implement cursor-based pagination suitable for infinite scroll.

Constraints:
- stable ordering
- index-friendly queries
- avoid OFFSET performance degradation
```

---

## MinIO Integration Prompt

```
Create an async-compatible storage adapter for MinIO.

Requirements:
- upload via multipart
- return public URL
- isolate client inside infrastructure layer
```

---

## Frontend FSD Structure Prompt

```
Create Vue 3 project structure using Feature-Sliced Design.

Layers:
app → pages → widgets → features → entities → shared

Avoid cross-layer imports.
```

---

## Refactoring Prompt Pattern

```
Refactor generated code to enforce separation between:
API layer
Application services
Repositories
Infrastructure
```

---

## Validation Prompt Pattern

```
Review the following code for architectural violations:
- framework leakage into domain
- sync database access
- transaction ownership mistakes
```

---

## Notes

Prompts evolved during development. Only representative examples are included here.
