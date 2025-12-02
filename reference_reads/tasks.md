# Tasks: Movie Data Web Scraping System

**Input**: Design documents from `/specs/001-movie-data-scraper/`

**Assumptions**:
- Language: Python 3.11 (inferred from common tooling and data-model SQL). Adjust if another language is required.
- Web/API framework: FastAPI + Uvicorn (lightweight, maps well to OpenAPI contract).
- DB layer: SQLAlchemy (or lightweight DB access) connecting to PostgreSQL.
- Scraping: requests + BeautifulSoup or HTTPX + lxml.

> If these assumptions are incorrect, adjust file names and dependencies accordingly.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

 - [x] T001 Create project directory structure: `C:\Users\skeer\OneDrive\Desktop\idk\src/`, `C:\Users\skeer\OneDrive\Desktop\idk\src\models/`, `C:\Users\skeer\OneDrive\Desktop\idk\src\services/`, `C:\Users\skeer\OneDrive\Desktop\idk\src\api/`, `C:\Users\skeer\OneDrive\Desktop\idk\src\config/`, `C:\Users\skeer\OneDrive\Desktop\idk\migrations/`, `C:\Users\skeer\OneDrive\Desktop\idk\tests/`, `C:\Users\skeer\OneDrive\Desktop\idk\docs/` — COMPLETED
 - [x] T002 Initialize Python dependency manifest at `C:\Users\skeer\OneDrive\Desktop\idk\requirements.txt` (include minimum: fastapi, uvicorn, sqlalchemy, psycopg[binary] or asyncpg, requests or httpx, beautifulsoup4, pydantic) — COMPLETED
 - [x] T003 [P] Create project README and `.gitignore` at `C:\Users\skeer\OneDrive\Desktop\idk\README.md` and `C:\Users\skeer\OneDrive\Desktop\idk\.gitignore` — COMPLETED
 - [x] T004 [P] Add environment config loader file `C:\Users\skeer\OneDrive\Desktop\idk\src\config\settings.py` (reads DB URL, rate limits, retry counts from env) — COMPLETED
 - [x] T005 [P] Add logging config file `C:\Users\skeer\OneDrive\Desktop\idk\src\config\logging.py` (structured JSON logging, file & console) — COMPLETED

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infra that MUST be complete before ANY user story

 - [x] T006 Create DB connection module `C:\Users\skeer\OneDrive\Desktop\idk\src\db\connection.py` (connect to PostgreSQL using env vars) — COMPLETED
 - [x] T007 Create migration SQL file `C:\Users\skeer\OneDrive\Desktop\idk\migrations\001_create_core_tables.sql` with table DDL for `movies`, `update_logs`, `batch_progress` (use SQL from `research/data-model.md`) — COMPLETED
 - [x] T008 [P] Create Movie model file `C:\Users\skeer\OneDrive\Desktop\idk\src\models\movie.py` (ORM model mapping to `public.movies` fields from data-model.md) — COMPLETED
 - [x] T009 [P] Create UpdateLog model file `C:\Users\skeer\OneDrive\Desktop\idk\src\models\update_log.py` (ORM model mapping to `public.update_logs`) — COMPLETED
 - [x] T010 [P] Create BatchProgress model file `C:\Users\skeer\OneDrive\Desktop\idk\src\models\batch_progress.py` (ORM model mapping to `public.batch_progress`) — COMPLETED
 - [x] T011 [P] Implement DB migration runner script `C:\Users\skeer\OneDrive\Desktop\idk\src\scripts\run_migrations.py` (applies SQL files in `migrations/` against configured DB) — COMPLETED
 - [x] T012 [P] Add utility for retry and exponential backoff `C:\Users\skeer\OneDrive\Desktop\idk\src\utils\retry.py` (configurable attempts up to 3, exponential backoff) — COMPLETED
 - [x] T013 [P] Add basic HTTP client helper `C:\Users\skeer\OneDrive\Desktop\idk\src\utils\http_client.py` (wraps requests/httpx and integrates rate limiting hooks) — COMPLETED
 - [x] T014 [P] Add index creation instruction and README for DB (`C:\Users\skeer\OneDrive\Desktop\idk\docs\db_indexes.md`) referencing `idx_movies_title_year` and `idx_movies_missing_data` — COMPLETED

**Checkpoint**: After Phase 2 completes, user-story implementation may begin.

---

## Phase 3: User Story 1 - Automated Movie Data Update (Priority: P1) 🎯 MVP

Goal: Automatically scrape Wikipedia for missing poster URLs, synopses, and film images and update the database.

Independent Test: Given a movie record with a missing poster_url or synopsis, running the batch scraper updates the `movies` record with values matching Wikipedia (manual verification or deterministic test against a test page).

Implementation tasks (priority order inside this story):

- [ ] T015 [P] [US1] Create scraper service module `C:\Users\skeer\OneDrive\Desktop\idk\src\services\scraper.py` (functions: fetch_wikipedia_page(title, year), parse_poster_url(html), parse_synopsis(html), parse_film_image_url(html))
- [ ] T016 [P] [US1] Create batch manager service `C:\Users\skeer\OneDrive\Desktop\idk\src\services\batch_manager.py` (start_batch(batch_size, rate_limit) -> iterates over missing-data movies, records BatchProgress entries)
- [ ] T017 [US1] Create update service `C:\Users\skeer\OneDrive\Desktop\idk\src\services\update_service.py` (apply validated scraped fields to DB; create UpdateLog entries with status and retry_count)
- [ ] T018 [US1] Implement API endpoint for starting a batch `C:\Users\skeer\OneDrive\Desktop\idk\src\api\scrape.py` - POST `/api/scrape/batch` per `contracts/api.yaml` (operationId: startBatch)
- [ ] T019 [US1] Implement API endpoint to manually trigger scraping for a movie `C:\Users\skeer\OneDrive\Desktop\idk\src\api\movies.py` - POST `/api/movies/{movieId}/scrape` (operationId: scrapeMovie)
- [ ] T020 [US1] Implement DB query helper `C:\Users\skeer\OneDrive\Desktop\idk\src\services\queries.py` to fetch next batch of movies missing poster_url or film_image_url (uses index `idx_movies_missing_data`)
- [ ] T021 [US1] Add integration wiring `C:\Users\skeer\OneDrive\Desktop\idk\src\main.py` to start FastAPI app and mount endpoints in `src/api/`
- [ ] T022 [US1] Add documentation snippet `C:\Users\skeer\OneDrive\Desktop\idk\docs\quickstart.md` for running a local batch and verifying updated movie record

Checkpoint: With the above implemented, you can run the POST `/api/scrape/batch` to trigger a batch run that updates `movies` records.

---

## Phase 4: User Story 2 - Data Validation (Priority: P2)

Goal: Ensure scraped data is validated before saving to DB (URL schemes, string lengths, enum/range checks).

Independent Test: Provide malformed data to the validation functions and verify invalid fields are rejected and only valid fields are written.

Implementation tasks:

- [ ] T023 [P] [US2] Create validation service `C:\Users\skeer\OneDrive\Desktop\idk\src\services\validator.py` (functions: is_valid_https_url(url), validate_imdb_rating(value), validate_synopsis(text))
- [ ] T024 [US2] Add validation configuration `C:\Users\skeer\OneDrive\Desktop\idk\src\config\validation.py` (max synopsis length, allowed year range, url rules)
- [ ] T025 [US2] Integrate validation into update flow `C:\Users\skeer\OneDrive\Desktop\idk\src\services\update_service.py` (use validator before writing fields; if partial validity: write valid fields only and log fallback)
- [ ] T026 [US2] Add a simple test harness `C:\Users\skeer\OneDrive\Desktop\idk\tests\unit\test_validator.py` (optional - skeleton for validating validator functions)

Checkpoint: Validation service ensures only acceptable fields are persisted; partial updates allowed per spec.

---

## Phase 5: User Story 3 - Error Handling and Logging (Priority: P3)

Goal: Robust error logging, retry handling, and observability for scraping and update processes.

Independent Test: Simulate network failures and verify retries occur (up to 3), that UpdateLog entries reflect retry_count, and that errors are logged.

Implementation tasks:

- [ ] T027 [P] [US3] Integrate retry/backoff into scraper calls `C:\Users\skeer\OneDrive\Desktop\idk\src\services\scraper.py` (use `C:\Users\skeer\OneDrive\Desktop\idk\src\utils\retry.py`)
- [ ] T028 [US3] Ensure UpdateLog entries are created for each attempt and final status `C:\Users\skeer\OneDrive\Desktop\idk\src\services\update_service.py` (write status: 'in_progress' -> 'success'/'failed')
- [ ] T029 [US3] Implement batch status endpoints `C:\Users\skeer\OneDrive\Desktop\idk\src\api\scrape.py` - GET `/api/scrape/batch/{batchId}` and DELETE `/api/scrape/batch/{batchId}` (per `contracts/api.yaml`)
- [ ] T030 [US3] Implement logs API `C:\Users\skeer\OneDrive\Desktop\idk\src\api\logs.py` - GET `/api/logs` to query UpdateLog entries (support filters: status, movieId, pagination)
- [ ] T031 [P] [US3] Add structured logging instrumentation to batch manager and update service `C:\Users\skeer\OneDrive\Desktop\idk\src\config\logging.py` and `C:\Users\skeer\OneDrive\Desktop\idk\src\services\batch_manager.py`

Checkpoint: Error scenarios produce UpdateLog entries and are visible via `/api/logs`; retries are applied automatically.

---

## Final Phase: Polish & Cross-Cutting Concerns

- [ ] T032 [P] Add skeleton unit and integration tests `C:\Users\skeer\OneDrive\Desktop\idk\tests\unit/` and `C:\Users\skeer\OneDrive\Desktop\idk\tests\integration/` (add one example test per service)
- [ ] T033 [P] Add CI workflow file at `C:\Users\skeer\OneDrive\Desktop\idk\.github\workflows\ci.yml` (runs lint and unit tests)
- [ ] T034 [P] Create `C:\Users\skeer\OneDrive\Desktop\idk\docs\runbook.md` for operations (how to run weekly batch, inspect logs, recover failed batches)
- [ ] T035 [P] Add security and robots.txt compliance check `C:\Users\skeer\OneDrive\Desktop\idk\src\utils\robots_checker.py` to ensure requests respect Wikipedia's robots.txt
- [ ] T036 [P] Update `C:\Users\skeer\OneDrive\Desktop\idk\README.md` with feature summary and MVP run instructions

---

## Dependencies & Execution Order

- Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3+ (User Stories in priority order or parallel after foundation)
- Story order (recommended): US1 (P1) → US2 (P2) → US3 (P3)

### Story Completion Order (dependency graph)
1. Foundation complete (T006-T014)
2. US1 (T015-T022) — MVP
3. US2 (T023-T026) — Validation
4. US3 (T027-T031) — Error handling & logging
5. Polish (T032-T036)

---

## Parallel Execution Examples

- While migrations are being prepared, the logging config and settings loader (T004, T005) can be implemented in parallel (they do not depend on DB schema).
- Model files (T008-T010) can be implemented in parallel with migration SQL (T007) because they are different files.
- Within US1, `src/services/scraper.py` (T015) and `src/services/queries.py` (T020) can be implemented in parallel by different devs (both are different files). Marked [P] accordingly.

---

## Implementation Strategy (MVP first)

MVP scope: Complete Setup (Phase 1) + Foundational (Phase 2) + User Story 1 (Phase 3) — tasks T001 through T022. This yields a runnable system able to run a scraping batch and update movie records.

Incremental delivery approach:
1. Execute Phase 1 tasks (T001-T005)
2. Execute Phase 2 tasks (T006-T014)
3. Implement US1 (T015-T022), validate independently
4. Add US2 and US3 iteratively (T023-T031)
5. Final polish (T032-T036)

---

## Validation Checklist (Format & Completeness)
- All tasks follow checklist format `- [ ] T### [P?] [US?] Description with file path`.
- Every user story phase includes a goal and independent test description.
- All contract endpoints from `contracts/api.yaml` are mapped to API tasks: `/api/scrape/batch` (T018), `/api/scrape/batch/{batchId}` (T029), `/api/movies/{movieId}/scrape` (T019), `/api/logs` (T030).

---

## Summary Report
- Path to generated tasks file: `C:\Users\skeer\OneDrive\Desktop\idk\specs\001-movie-data-scraper\tasks.md`
- Total tasks: 36
- Tasks per story:
  - Setup/Foundational (Phases 1-2): 14 tasks (T001-T014)
  - US1 (P1): 8 tasks (T015-T022)
  - US2 (P2): 4 tasks (T023-T026)
  - US3 (P3): 5 tasks (T027-T031)
  - Final/Polish: 5 tasks (T032-T036)
- Parallel opportunities identified: Many [P]-marked tasks (see checklist). Notable parallelizable work: logging, config, model files, validator, HTTP client, unit tests.
- Independent test criteria per story:
  - US1: Given a movie with missing fields, run batch and verify `movies` updated matching Wikipedia.
  - US2: Validator rejects malformed fields; only valid fields persist.
  - US3: Simulated network failures lead to retries; UpdateLog captures retry_count and final status.
- Suggested MVP scope: User Story 1 (T015-T022) plus foundational tasks (T006-T014).
- Format validation: All tasks created follow the required checklist format with Task IDs, [P] where applicable, [USx] for story tasks, and exact file paths.

---

If you'd like, I can now:
- Create the minimal `requirements.txt` and `src/config/settings.py` files (I already listed them as tasks) and open the first implementation files for T006-T010, or
- Generate the CI workflow and basic test skeletons (T032, T033).

Which next step do you want me to take (start implementing the MVP files, scaffold the tests, or something else)?
