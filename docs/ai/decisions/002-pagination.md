# ADR 002 — Pagination Strategy

## Status

Accepted

## Context

Main page requires infinite scroll with 100+ products.

Offset pagination degrades with dataset growth.

## Decision

Use cursor-based pagination.

Ordering based on stable column (created_at, id).

Indexes added to support query efficiency.

## Consequences

Positive:

* scalable pagination
* stable ordering
* avoids large OFFSET scans

Negative:

* slightly more complex API contract
