-- Create movies table
CREATE TABLE IF NOT EXISTS public.movies (
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

CREATE UNIQUE INDEX IF NOT EXISTS idx_movies_title_year ON public.movies(title, release_year);
CREATE INDEX IF NOT EXISTS idx_movies_missing_data ON public.movies(id) WHERE poster_url IS NULL OR film_image_url IS NULL;

-- Create update_logs table
CREATE TABLE IF NOT EXISTS public.update_logs (
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

CREATE INDEX IF NOT EXISTS idx_update_logs_movie ON public.update_logs(movie_id);
CREATE INDEX IF NOT EXISTS idx_update_logs_status ON public.update_logs(status);

-- Create batch_progress table
CREATE TABLE IF NOT EXISTS public.batch_progress (
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

CREATE INDEX IF NOT EXISTS idx_batch_progress_status ON public.batch_progress(status);
CREATE INDEX IF NOT EXISTS idx_batch_progress_batch_id ON public.batch_progress(batch_id);
