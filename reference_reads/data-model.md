# Data Model Documentation

## Core Entities

### Movie
The primary entity representing a movie in the database.

```sql
CREATE TABLE public.movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    language VARCHAR(50),
    release_year INTEGER,
    imdb_rating DECIMAL(3,1),
    poster_url TEXT,
    synopsis TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    budget_crores DECIMAL(10,2),
    gross_crores DECIMAL(10,2),
    film_image_url TEXT
);
```

#### Field Descriptions
- `id`: Unique identifier for the movie
- `title`: Movie title (required)
- `genre`: Movie genre classification
- `language`: Primary language of the movie
- `release_year`: Year of movie release
- `imdb_rating`: IMDB rating (0.0-10.0)
- `poster_url`: URL to movie poster image
- `synopsis`: Movie plot summary
- `created_at`: Record creation timestamp
- `budget_crores`: Movie budget in crores
- `gross_crores`: Movie gross earnings in crores
- `film_image_url`: URL to film promotional image

#### Validation Rules
1. Title and release year combination must be unique
2. URLs must be valid HTTPS URLs
3. Release year must be between 1900 and current year
4. IMDB rating must be between 0.0 and 10.0
5. Synopsis must not exceed 2000 characters

### UpdateLog
Tracks all update operations and their status.

```sql
CREATE TABLE public.update_logs (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES public.movies(id),
    operation_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_status CHECK (status IN ('success', 'failed', 'in_progress'))
);
```

#### Field Descriptions
- `id`: Unique identifier for the log entry
- `movie_id`: Reference to the updated movie
- `operation_type`: Type of update operation
- `status`: Current status of the operation
- `error_message`: Details of any errors encountered
- `retry_count`: Number of retry attempts
- `created_at`: When the operation started
- `updated_at`: Last status update timestamp

#### Validation Rules
1. Status must be one of: 'success', 'failed', 'in_progress'
2. Retry count must not exceed 3
3. Error message required if status is 'failed'

### BatchProgress
Tracks progress of batch processing operations.

```sql
CREATE TABLE public.batch_progress (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR(36) NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    total_records INTEGER NOT NULL,
    processed_records INTEGER DEFAULT 0,
    status VARCHAR(20) NOT NULL,
    last_processed_id INTEGER,
    CONSTRAINT valid_batch_status CHECK (status IN ('running', 'completed', 'failed', 'paused'))
);
```

#### Field Descriptions
- `id`: Unique identifier for the batch
- `batch_id`: UUID for the batch process
- `start_time`: When the batch started
- `end_time`: When the batch completed
- `total_records`: Total records to process
- `processed_records`: Number of records processed
- `status`: Current batch status
- `last_processed_id`: Last movie ID processed

#### Validation Rules
1. Processed records must not exceed total records
2. End time must be after start time when present
3. Status must be one of: 'running', 'completed', 'failed', 'paused'

## Relationships
1. UpdateLog.movie_id → Movie.id (Many-to-One)
   - Each movie can have multiple update log entries
   - Cascade delete disabled to preserve audit trail

## Indexes
1. Movies:
   ```sql
   CREATE INDEX idx_movies_title_year ON public.movies(title, release_year);
   CREATE INDEX idx_movies_missing_data ON public.movies(id) WHERE poster_url IS NULL OR film_image_url IS NULL;
   ```

2. UpdateLog:
   ```sql
   CREATE INDEX idx_update_logs_movie ON public.update_logs(movie_id);
   CREATE INDEX idx_update_logs_status ON public.update_logs(status);
   ```

3. BatchProgress:
   ```sql
   CREATE INDEX idx_batch_progress_status ON public.batch_progress(status);
   CREATE INDEX idx_batch_progress_batch_id ON public.batch_progress(batch_id);
   ```