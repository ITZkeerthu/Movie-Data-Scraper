# Database Indexes

This document lists recommended indexes for `public.movies`, `public.update_logs`, and `public.batch_progress` used by the movie-data-scraper feature.

- `idx_movies_title_year` on `(title, release_year)` — used for exact title+year lookups
- `idx_movies_missing_data` on `id WHERE poster_url IS NULL OR film_image_url IS NULL` — used to find candidates for scraping
- `idx_update_logs_movie` on `movie_id` — speeds queries for logs per movie
- `idx_update_logs_status` on `status` — used for log filtering
- `idx_batch_progress_status` on `status` — used for monitoring batch states
- `idx_batch_progress_batch_id` on `batch_id` — lookup by batch UUID

These indexes are created in `migrations/001_create_core_tables.sql`. If you use a migration tool (Alembic), convert the SQL above into migration scripts accordingly.
