# socmed-analyst

Social media analyst for local government (Kabupaten Pasuruan). This tool analyzes TikTok comment data to extract citizen complaints, suggestions, and appreciation, generating formal executive summary PDF reports for the Regent (Bupati).

## Features

- AI-powered topic extraction and keyword identification from natural language input.
- TikTok comment scraping integration via Apify.
- Intelligent comment filtering by keywords and date range.
- Core issue extraction with categorization: valid complaints, suggested questions/solutions, and appreciation.
- Automated OPD (Organisasi Perangkat Daerah) routing to identify the responsible government agency.
- Formal executive summary generation in professional government report format.
- PDF report output via WeasyPrint.
- Asynchronous task processing with Celery and Redis.

## Tech Stack

- Runtime: Python 3.13
- Web Framework: FastAPI + Uvicorn
- Database: SQLite via SQLModel (SQLAlchemy ORM)
- Migrations: Alembic
- Task Queue: Celery with Redis broker
- AI/LLM: OpenAI SDK (via OpenRouter with Gemini model)
- Scraping: Apify Client (TikTok actor)
- PDF Generation: WeasyPrint
- API Documentation: Scalar
- Configuration: Pydantic Settings with dotenv
- Package Manager: uv

## Project Structure

- app/ - Main application code
  - main.py - FastAPI entry point and route definitions
  - celery_app.py - Celery worker configuration and task discovery
  - analyze/ - Core analysis pipeline
    - task.py - Celery task for end-to-end analysis
    - method.py - Implementation logic for data extraction and processing
    - prompt.py - System prompts for AI analysis
    - schema.py - Pydantic models for request/response validation
  - core/ - Application settings and configuration
  - models/ - SQLModel database models and engine setup
  - utils/ - External service clients (OpenAI, Apify)
- alembic/ - Database migration scripts and environment
- seed_data/ - Initial dataset (JSON/SQL) and seeding scripts
- Makefile - Command shortcuts for development and workers
- pyproject.toml - Project dependencies and metadata

## Prerequisites

- Python 3.13+
- uv (Python package manager)
- Redis server (running on localhost:6379)
- System dependencies for WeasyPrint (cairo, pango, gdk-pixbuf, libffi)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd socmed-analyst
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Configure environment variables:
   Copy the example environment file and fill in your API keys:

   ```bash
   cp .env.example .env
   # Edit .env with your OPENROUTER_API_KEY and APIFY_API_KEY
   ```

4. Run database migrations:

   ```bash
   uv run alembic upgrade head
   ```

5. Seed initial data (optional):
   ```bash
   uv run python seed_data/seed_all.py
   ```

## Environment Variables

| Variable            | Description                        | Required |
| ------------------- | ---------------------------------- | -------- |
| APP_NAME            | Name of the application            | Yes      |
| VERSION             | Application version                | Yes      |
| DATABASE_URL        | Connection string for SQLite       | Yes      |
| OPENROUTER_API_KEY  | API key for OpenRouter             | Yes      |
| OPENROUTER_BASE_URL | Base URL for OpenRouter API        | Yes      |
| APIFY_API_KEY       | API key for Apify                  | Yes      |
| REDIS_URL           | Connection string for Redis broker | Yes      |

## Usage

Start the FastAPI development server:

```bash
make dev
```

In a separate terminal, start the Celery worker:

```bash
make celery
```

The API will be available at http://localhost:8000. You can view the interactive API documentation at:

- Scalar: http://localhost:8000/scalar
- Swagger UI: http://localhost:8000/docs

### Submitting an Analysis

Send a POST request to `/analyze` with a topic:

```bash
curl -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"topic": "masalah jalan rusak di Grati bulan lalu"}'
```

## API Endpoints

- GET / - Health check and welcome message.
- POST /analyze - Accepts a topic string to trigger an asynchronous analysis task.
- GET /scalar - Renders the Scalar API reference.

## Database Schema

The application uses the following primary modules:

- WilayahKecamatan / WilayahDesa - Hierarchical regional data for Kabupaten Pasuruan.
- TikTokUser - Profiles of prioritized TikTok accounts.
- TikTokVideo - Metadata for scraped videos.
- TikTokComment - Raw comment data used for thematic analysis.
- OrganisasiPerangkatDaerah (OPD) - Government agencies mapped to specific issue categories.

## How It Works

1. User Inquiry: A topic is submitted via the API.
2. Intent Extraction: AI parses the topic to identify keywords, specific locations, and date filters.
3. Data Retrieval: The system queries the SQLite database for relevant TikTok comments based on the extracted intent.
4. Issue Analysis: AI categorizes comments into valid complaints, suggestions, and appreciation.
5. Agency Routing: AI identifies the most relevant OPD to handle the identified issues.
6. Report Generation: AI synthesizes the data into a formal executive summary in Indonesian.
7. PDF Rendering: WeasyPrint converts the markdown summary into a professional PDF document.

## License

This project is licensed under the terms of the MIT license.
