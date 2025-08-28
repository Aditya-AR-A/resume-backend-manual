# Resume Backend API (Manual Implementation)

A FastAPI-based backend service for a portfolio/resume website with AI-powered chat functionality.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **AI Integration**: Support for multiple LLM providers (Groq, OpenAI, Anthropic)
- **Portfolio Data**: RESTful endpoints for projects, experience, certificates
- **Custom Logging**: Enhanced logging with colored console output and file logging
- **CORS Support**: Configurable CORS middleware
- **Health Checks**: Built-in health check endpoints
- **Configuration Management**: Pydantic-based settings with environment variable support

## Project Structure

```
backend-manual/
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Application configuration
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── custom.py            # Custom middleware
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── prompts.yaml         # AI prompts configuration
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── ai_routes.py         # AI chat endpoints
│   │   ├── data_routes.py       # Data retrieval endpoints
│   │   └── main_routes.py       # Health and status endpoints
│   ├── services/
│   │   └── __init__.py          # Business logic (to be implemented)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py            # Custom logging utility
│   ├── __init__.py
│   └── main.py                  # FastAPI application
├── data/                        # JSON data files
├── tests/                       # Test files (to be implemented)
├── requirements.txt             # Python dependencies
└── README.md
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend-manual
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env  # Create from template if available
   ```

   Configure the following in your `.env` file:
   ```env
   # Application
   SECRET_KEY=your-secret-key-here

   # AI Providers (at least one required)
   GROQ_API_KEY=your-groq-api-key
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key

   # Database (optional)
   DB_URL=sqlite:///./resume.db

   # Cache (optional)
   CACHE_URL=redis://localhost:6379
   ```

## Usage

### Development

```bash
# Run with auto-reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
# Run without reload
python -m app.main

# Or using uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health & Status
- `GET /` - Welcome message
- `GET /api/v1/health` - Health check
- `GET /api/v1/status` - Application status
- `GET /api/v1/config` - Configuration info

### Data Endpoints
- `GET /api/v1/data/profile` - Portfolio profile
- `GET /api/v1/data/intro` - Introduction data
- `GET /api/v1/data/layout` - Layout configuration
- `GET /api/v1/data/projects` - List projects (with filtering)
- `GET /api/v1/data/projects/{id}` - Get specific project
- `GET /api/v1/data/experience` - Work experience
- `GET /api/v1/data/certificates` - Certificates

### AI Endpoints
- `POST /api/v1/ai/chat` - Chat with AI assistant
- `POST /api/v1/ai/classify` - Classify user messages
- `GET /api/v1/ai/status` - AI system status

## Configuration

The application uses Pydantic settings with the following configuration sources (in order of precedence):
1. Environment variables
2. `.env` file
3. `.env.local` file
4. Default values

### Key Settings

- **Application**: `APP_NAME`, `APP_VERSION`, `DEBUG`, `HOST`, `PORT`
- **AI Providers**: `GROQ_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
- **Database**: `DB_URL`, `DB_POOL_SIZE`
- **Cache**: `CACHE_ENABLED`, `CACHE_URL`, `CACHE_TTL`
- **Logging**: `LOG_LEVEL`, `LOG_DIR`

## Data Files

The application expects JSON data files in the `data/` directory:
- `page.json` - Main page configuration
- `intro.json` - Introduction content
- `layout.json` - Layout settings
- `projects.json` - Projects data
- `jobs.json` - Work experience
- `certificates.json` - Certificates

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
# Using black
black app/

# Using isort for imports
isort app/
```

### API Documentation
When running, visit `http://localhost:8000/docs` for interactive API documentation.

## Deployment

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production
```env
DEBUG=false
RELOAD=false
SECRET_KEY=your-production-secret-key
# ... other production settings
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]
