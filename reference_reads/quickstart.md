# Movie Data Scraper Quickstart Guide

## Overview
This system automatically scrapes movie data from Wikipedia and updates the PostgreSQL database with missing information such as poster URLs, synopses, and film images.

## Prerequisites
1. PostgreSQL database access with credentials
2. Wikipedia API access (MediaWiki API)
3. Network access to Wikipedia and database server

## Configuration

### Environment Variables
```bash
# Database Configuration
DB_HOST=<database_host>
DB_PORT=5432
DB_NAME=movie_rating_system
DB_USER=129141
DB_PASSWORD=<your_password>

# Wikipedia API Configuration
WIKI_API_USER_AGENT=<your_app_name>
WIKI_API_EMAIL=<your_email>

# Batch Processing
BATCH_SIZE=100
MAX_RETRIES=3
BASE_RATE_LIMIT=1
```

## Usage

### Starting a Batch Process
To start a new batch scraping process:
```bash
curl -X POST http://localhost:8080/api/scrape/batch
```

### Checking Batch Status
To check the status of a running batch:
```bash
curl http://localhost:8080/api/scrape/batch/{batchId}
```

### Manual Movie Update
To trigger scraping for a specific movie:
```bash
curl -X POST http://localhost:8080/api/movies/{movieId}/scrape
```

### Viewing Logs
To view update operation logs:
```bash
curl http://localhost:8080/api/logs?status=failed
```

## Monitoring
- Monitor batch progress through the API endpoints
- Check update logs for any failures
- View database statistics for completed updates

## Troubleshooting

### Common Issues
1. Rate Limiting
   - Error: "Rate limit exceeded"
   - Solution: Check base rate configuration and adjust if needed

2. Database Connection
   - Error: "Connection refused"
   - Solution: Verify database credentials and network access

3. Missing Wikipedia Pages
   - Error: "Page not found"
   - Solution: Check movie title and year matching

### Support
For technical support or issues:
1. Check the update logs for specific error messages
2. Review batch progress status
3. Contact database administrator for access issues