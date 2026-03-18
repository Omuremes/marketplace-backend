# ADR 003 — Image Storage Strategy

## Status

Accepted

## Context

Images must be stored outside application containers.

Requirement specifies S3-compatible storage.

## Decision

Use MinIO as local S3-compatible storage.

Backend stores object keys in database.

Public URLs used for prototype simplicity.

Future upgrade path:

* presigned URLs
* private buckets

## Consequences

Positive:

* production-like storage architecture
* easy local reproducibility

Negative:

* simplified access control
