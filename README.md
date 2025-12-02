# Movie Data Web Scraper

![Movie Data Scraper](image.png)

A FastAPI-based web scraping system that automatically fetches and updates movie data from Wikipedia, including poster URLs, synopses, and film images, storing them in a PostgreSQL database.

## Features

- 🎬 Automated batch scraping of movie data from Wikipedia
- 📊 PostgreSQL database with optimized indexes for fast queries
- 🔄 Retry mechanism with exponential backoff for network resilience
- ⚡ Rate-limited HTTP client to respect Wikipedia's guidelines
- 📝 Comprehensive logging and error tracking
- 🚀 RESTful API with interactive Swagger documentation

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```powershell
   git clone <repository-url>
   cd idk
   ```

2. **Set up Python virtual environment**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy `.env.example` to `.env` and update with your database credentials:
   ```
   DATABASE_URL=postgresql://postgres:129141@localhost:5432/movie_rating_system
   WIKIPEDIA_RATE_LIMIT=1.0
   RETRY_COUNT=3
   BATCH_SIZE=100
   LOG_LEVEL=INFO
   ```

5. **Run database migrations**
   ```powershell
   $env:DATABASE_URL="postgresql://postgres:129141@localhost:5432/movie_rating_system"
   python src/scripts/run_migrations_run.py
   ```

6. **Start the Backend Server**

   ```powershell
   $env:DATABASE_URL="postgresql://postgres:129141@localhost:5432/movie_rating_system"
   python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend API will be available at:
   - Main API: <http://localhost:8000/>
   - Interactive Docs: <http://localhost:8000/docs>
   - ReDoc: <http://localhost:8000/redoc>

## Running the Application

### Backend Only (Current Setup)

This project is currently a **backend-only API service**. To run it:

```powershell
# Set environment variable and start the server
$env:DATABASE_URL="postgresql://postgres:129141@localhost:5432/movie_rating_system"
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Access the interactive API documentation at <http://localhost:8000/docs> to test endpoints directly in your browser.

### Frontend + Backend (Future)

*Note: This project does not currently include a frontend. The API is designed to be consumed by any frontend framework.*

To add a frontend in the future:

1. **Create a frontend directory** (e.g., `frontend/`)
2. **Choose a framework** (React, Vue, Angular, etc.)
3. **Install dependencies** in the frontend folder
4. **Configure API calls** to point to `http://localhost:8000`
5. **Run both servers**:

   ```powershell
   # Terminal 1 - Backend
   $env:DATABASE_URL="postgresql://postgres:129141@localhost:5432/movie_rating_system"
   python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

   # Terminal 2 - Frontend (example for React)
   cd frontend
   npm run dev
   ```

### Using the API

You can interact with the backend through:
- **Swagger UI**: <http://localhost:8000/docs> (recommended for testing)
- **cURL**: Command-line HTTP requests
- **Postman**: API testing tool
- **Custom Frontend**: Build your own UI that calls these endpoints

## API Endpoints

### Scraping Operations

- **POST** `/api/scrape/batch` - Start a new batch scraping process
  - Query params: `batch_size` (default: 100), `rate_limit` (default: 1.0)
  - Returns: `batchId` and status

- **POST** `/api/movies/{movieId}/scrape` - Manually scrape a specific movie
  - Path param: `movieId` (integer)
  - Returns: Updated fields and status

- **GET** `/api/scrape/batch/{batchId}` - Get batch process status *(planned)*

- **DELETE** `/api/scrape/batch/{batchId}` - Cancel a running batch *(planned)*

- **GET** `/api/logs` - Query update logs *(planned)*
  - Query params: `status`, `movieId`, `page`, `pageSize`

## Project Structure

```
idk/
├── src/
│   ├── api/           # API endpoints
│   ├── config/        # Configuration and settings
│   ├── db/            # Database connection
│   ├── models/        # SQLAlchemy ORM models
│   ├── services/      # Business logic
│   ├── scripts/       # Utility scripts
│   └── utils/         # Helper utilities
├── migrations/        # Database migration SQL files
├── reference_reads/   # Documentation and specifications
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Database Schema

The system uses three main tables:

- **movies** - Stores movie information (title, year, poster_url, synopsis, etc.)
- **update_logs** - Tracks all update operations and errors
- **batch_progress** - Monitors batch processing status

See `reference_reads/db_indexes.md` for index details.

## Development

### Running Tests *(planned)*
```powershell
pytest tests/
```

### Code Quality
- Linting: Follow PEP 8 standards
- Type hints: Encouraged for better IDE support

## Configuration

Environment variables can be set in `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | Required |
| WIKIPEDIA_RATE_LIMIT | Requests per second | 1.0 |
| RETRY_COUNT | Max retry attempts | 3 |
| BATCH_SIZE | Movies per batch | 100 |
| LOG_LEVEL | Logging level | INFO |

## How It Works

1. **Batch Processing**: The system identifies movies with missing data (poster_url or film_image_url)
2. **Wikipedia Scraping**: Fetches movie pages from Wikipedia using title and year
3. **Data Parsing**: Extracts poster URLs, synopses, and film images using BeautifulSoup
4. **Database Update**: Validates and stores scraped data with comprehensive logging
5. **Error Handling**: Retries failed requests with exponential backoff

## Contributing

This is a feature implementation project. See `reference_reads/tasks.md` for implementation progress and next steps.

## License

[Your License Here]

## Documentation

Additional documentation is available in the `reference_reads/` folder:
- `quickstart.md` - Detailed setup guide
- `tasks.md` - Implementation task list
- `spec.md` - Feature specification
- `plan.md` - Technical plan
- `db_indexes.md` - Database optimization guide

## Support

For issues and questions, please refer to the project documentation or create an issue in the repository.
