# ADR 001 — Backend Architecture

## Status

Accepted

## Context

The project required a production-oriented prototype using FastAPI with AI-assisted development.

A simple CRUD structure would not demonstrate architectural control.

## Decision

Adopt layered architecture:

* API (HTTP boundary)
* Application services
* Domain entities
* Repository abstraction
* Infrastructure adapters

Unit of Work introduced for transactional consistency.

## Consequences

Positive:

* clear separation of concerns
* testable services
* AI output easier to validate

Negative:

* slightly higher initial complexity
* additional mapping layer required
