# EventHub API Stages 1-9 Audit Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit and, where necessary, minimally correct EventHub API Stages 1-9, seed the current PostgreSQL database, verify the API, and save the evidence in `DRF_STAGES_1_9_AUDIT_REPORT.md`.

**Architecture:** Preserve the current Django/DRF application structure. Inspect each completed learning stage against the supplied specification, make only small correctness fixes within Stages 1-9, verify against Docker PostgreSQL and Redis, and document exact outcomes without implementing permissions.

**Tech Stack:** Python 3.13, Django 6, Django REST Framework, SimpleJWT, PostgreSQL 17, Redis 7, Docker Compose.

**Spec:** `/Users/dima/.codex/attachments/e8ea0a2a-885e-4d11-98e7-5c9f0e0f004d/pasted-text.txt`

## Global Constraints

- Do not implement Stage 10 permissions, ownership rules, or Stage 11+ functionality.
- Do not containerize the Django application.
- Preserve the evolved ViewSet/router architecture; do not restore superseded tutorial views.
- Only fix Critical or Important issues that are small, unambiguous, and belong to Stages 1-9.
- Do not modify sibling projects.
- Do not record passwords or JWTs in the report.

---

### Task 1: Static Stage Audit

**Files:**
- Inspect: `config/settings.py`, `config/urls.py`, `api/*.py`, `accounts/*.py`
- Inspect: `api/migrations/*.py`, `accounts/migrations/*.py`
- Inspect: `docker-compose.yml`, `Makefile`

**Interfaces:**
- Consumes: supplied Stages 1-9 specification.
- Produces: a list of verified requirements and categorized findings.

- [x] Inspect models, serializers, views, URLs, settings, migrations, imports, debug code, and Docker services.
- [x] Search for obsolete auth imports, superseded DRF classes, duplicate URLs, debug statements, and dead imports.
- [x] Compare model constraints and migration state with their names and intended conditions.

### Task 2: Baseline Verification

**Files:**
- Test: `accounts/tests.py`
- Test: `api/tests.py`

**Interfaces:**
- Consumes: existing Django settings and Docker Compose services.
- Produces: check, migration, test, PostgreSQL, and Redis status evidence.

- [x] Run the Makefile commands and direct Django checks appropriate to the repository.
- [x] Confirm migration graph and applied migration status against PostgreSQL.
- [x] Confirm PostgreSQL and Redis services are reachable.

### Task 3: Minimal Correctness Fixes

**Files:**
- Modify only files implicated by Critical or Important findings.
- Test: the existing app test modules nearest each fix.

**Interfaces:**
- Consumes: categorized findings from Tasks 1-2.
- Produces: minimal tested corrections restricted to Stages 1-9.

- [x] Add a focused failing test for each confirmed behavioral defect.
- [x] Run the focused test and verify the expected failure.
- [x] Apply the smallest implementation change that fixes the defect.
- [x] Re-run focused tests, `manage.py check`, and migration checks.

### Task 4: PostgreSQL Seed Data

**Files:**
- No source file changes; write records through Django ORM.

**Interfaces:**
- Consumes: `accounts.User`, `api.Category`, and `api.Event` models.
- Produces: two named users, two categories, and at least three future events in the current PostgreSQL database.

- [x] Create or update `organizer1` and `attendee1` through `create_user()` semantics without exposing passwords.
- [x] Create or update Backend and Community categories with unique slugs.
- [x] Create or update the three specified events with future `starts_at` values.
- [x] Record database IDs for the audit report.

### Task 5: End-to-End API Verification

**Files:**
- No source file changes; exercise the configured API through DRF's test client against PostgreSQL.

**Interfaces:**
- Consumes: seeded database records and configured routes.
- Produces: expected/actual status evidence for registration, JWT, refresh, and Event CRUD.

- [x] Verify registration, password omission, role persistence, JWT issuance, authenticated user resolution, and token refresh.
- [x] Verify Event list, retrieve, create, partial update, full update, and delete.
- [x] Clean up only temporary API verification records while preserving the requested seed data.

### Task 6: Audit Report

**Files:**
- Create: `DRF_STAGES_1_9_AUDIT_REPORT.md`

**Interfaces:**
- Consumes: all findings, command outputs, seed IDs, API statuses, and changed-file list.
- Produces: the required permanent audit record and Stage 10 readiness conclusion.

- [x] Write every required report section, including expected missing permissions and ownership.
- [x] List Critical, Important, and Optional findings separately.
- [x] State `READY FOR STAGE 10` only if checks and required API flows pass after fixes.
- [x] Verify that the report contains no passwords or token values.
