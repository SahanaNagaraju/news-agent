# News Agent

A standalone news agent service built with Python and FastAPI that integrates with newdata.io to fetch and serve news articles. Can be deployed on Render, BTP, or any Python hosting platform.

## Features

- 🌐 **RESTful API** for news retrieval
- 🔌 **Newdata.io Integration** for comprehensive news data
- ☁️ **Cloud Ready** - Deploy to Render, BTP, or other platforms
- 🐍 **Python/FastAPI** - Modern, fast, and async
- 🔒 **Security** - CORS support and environment-based configuration
- 📊 **Health Monitoring** endpoint for service status
- 🚀 **Production Ready** with proper error handling
- 📝 **Auto-generated API Documentation** via FastAPI
- 📖 **Interactive API Docs** at `/docs` endpoint

## Architecture

The application is structured as a microservice with the following components:

```
news-agent/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── config.py        # Configuration management
│   ├── models.py        # Pydantic models
│   ├── services/        # Business logic (newdata.io integration)
│   │   ├── __init__.py
│   │   └── newdata_service.py
│   └── routes/          # API route definitions
│       ├── __init__.py
│       └── news.py
├── deployment/          # Deployment guides
│   ├── render-deployment-guide.md
│   └── btp-deployment-guide.md
├── run.py               # Local development server
├── requirements.txt     # Python dependencies
├── Procfile             # Process file for deployment
└── .env.example         # Example environment variables
```

## Prerequisites

- Python >= 3.11
- pip
- Newdata.io API key
- (For deployment) Render or BTP account

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SahanaNagaraju/news-agent.git
   cd news-agent
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env` and add your newdata.io API key:
   ```
   NEWDATA_API_KEY=your_api_key_here
   ```

## Running Locally

### Development Mode
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

The server will start on `http://localhost:8080`.

### Access API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8080/docs
- **Alternative Docs**: http://localhost:8080/redoc
- **Root Endpoint**: http://localhost:8080/

## API Endpoints

### Root Endpoint
```
GET /
```
Returns service information and available endpoints.

### Health Check
```
GET /health
```
Returns service health status including newdata.io connectivity.

### Fetch News
```
GET /api/news?query=technology&category=tech&country=us&language=en&limit=10
```
**Query Parameters:**
- `query` (optional): Search query term
- `category` (optional): News category (e.g., business, technology, sports)
- `country` (optional): Country code (e.g., us, uk, in)
- `language` (optional): Language code (default: en)
- `limit` (optional): Number of results (default: 10)

**Example Response:**
```json
{
  "success": true,
  "data": {
    "articles": [...]
  },
  "timestamp": "2026-09-02T08:12:38.000Z"
}
```

### Fetch Headlines
```
GET /api/headlines?category=business&country=us&limit=10
```
**Query Parameters:**
- `category` (optional): News category
- `country` (optional): Country code (default: us)
- `limit` (optional): Number of results (default: 10)

### Search by Topic
```
GET /api/search/:topic?country=us&language=en&limit=10
```
**Path Parameters:**
- `topic` (required): Topic to search for

**Query Parameters:**
- `country` (optional): Country code
- `language` (optional): Language code
- `limit` (optional): Number of results (default: 10)

**Example:**
```bash
curl http://localhost:8080/api/search/climate-change?limit=5
```

### Complex Query (POST)
```
POST /api/news/query
Content-Type: application/json

{
  "query": "artificial intelligence",
  "category": "technology",
  "country": "us",
  "language": "en",
  "limit": 20
}
```

## Example Usage

### Using cURL

```bash
# Get headlines
curl http://localhost:8080/api/headlines?country=us&limit=5

# Search for news
curl http://localhost:8080/api/news?query=climate+change&limit=10

# Search by topic
curl http://localhost:8080/api/search/technology?country=in

# Complex query (POST)
curl -X POST http://localhost:8080/api/news/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "space exploration",
    "category": "science",
    "limit": 15
  }'
```

### Using JavaScript (Fetch API)

```javascript
// Fetch headlines
fetch('http://localhost:8080/api/headlines?country=us&limit=5')
  .then(response => response.json())
  .then(data => console.log(data));

// Complex query
fetch('http://localhost:8080/api/news/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'renewable energy',
    category: 'environment',
    limit: 10
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Deployment

### Deploy to Render (Recommended)

For detailed deployment instructions, see [Render Deployment Guide](deployment/render-deployment-guide.md).

**Quick Deploy:**
1. Push your code to GitHub
2. Connect to Render
3. Create a new Web Service
4. Set environment variables
5. Deploy!

See the full guide: [deployment/render-deployment-guide.md](deployment/render-deployment-guide.md)

### Deploy to BTP

For BTP deployment, see [BTP Deployment Guide](deployment/btp-deployment-guide.md).

**Quick Deploy:**
```bash
cf login
cf set-env news-agent NEWDATA_API_KEY "your_api_key_here"
cf push -f manifest.yml
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Server port | 8080 | No |
| `ENV` | Environment mode | production | No |
| `NEWDATA_API_KEY` | Newdata.io API key | - | Yes |
| `NEWDATA_API_URL` | Newdata.io API base URL | https://api.newdata.io/v1 | No |
| `APP_NAME` | Application name | news-agent | No |
| `LOG_LEVEL` | Logging level | info | No |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | * | No |

## External Integration

This news agent can be called from external applications, including other agents:

### Python Example
```python
import requests

# Your deployed service URL
NEWS_AGENT_URL = "https://news-agent.onrender.com"  # or your BTP URL

# Fetch news
response = requests.get(f"{NEWS_AGENT_URL}/api/news", params={"query": "technology"})
news = response.json()

# Get headlines
response = requests.get(f"{NEWS_AGENT_URL}/api/headlines", params={"country": "us"})
headlines = response.json()
```

### JavaScript Example
```javascript
// Example: Calling from another agent
const newsAgent = {
  baseUrl: 'https://news-agent.onrender.com',  // or your BTP URL
  
  async getNews(query) {
    const response = await fetch(`${this.baseUrl}/api/news?query=${query}`);
    return await response.json();
  },
  
  async getHeadlines(country = 'us') {
    const response = await fetch(`${this.baseUrl}/api/headlines?country=${country}`);
    return await response.json();
  }
};

// Usage
const news = await newsAgent.getNews('technology');
console.log(news);
```

## Security

- **FastAPI Security**: Built-in security features
- **CORS**: Configurable origin restrictions
- **Environment Variables**: Sensitive data stored securely
- **HTTPS**: Enforced on Render/BTP deployment
- **Input Validation**: Pydantic models validate all inputs
- **API Documentation**: Auto-generated and interactive

## Monitoring

### Health Check
```bash
curl http://localhost:8080/health
```

### Application Logs
```bash
# Local
python run.py

# Render: View in Dashboard under "Logs" tab

# BTP
cf logs news-agent --recent
```

## Error Handling

All API endpoints return consistent error responses:

```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "details": "Additional details"
  },
  "timestamp": "2026-09-02T08:12:38.000Z"
}
```

## Development

### Project Structure

- **app/config.py**: Configuration and environment variable management
- **app/services/**: Business logic for newdata.io integration
- **app/routes/**: API route definitions and handlers
- **app/models.py**: Pydantic models for request/response validation
- **app/main.py**: FastAPI application entry point
- **run.py**: Local development server
- **requirements.txt**: Python dependencies

### Adding New Features

1. Create service logic in `app/services/`
2. Define routes in `app/routes/`
3. Create/update Pydantic models in `app/models.py`
4. Update documentation in README.md
5. Test locally before deploying

### Code Quality

```bash
# Format code
pip install black
black app/

# Type checking
pip install mypy
mypy app/

# Linting
pip install flake8
flake8 app/
```

## Troubleshooting

### Common Issues

**Issue**: Application won't start
- Check if `NEWDATA_API_KEY` is set correctly
- Verify port 8080 is available
- Check logs for specific errors

**Issue**: No response from newdata.io
- Verify API key is valid
- Check internet connectivity
- Review newdata.io service status

**Issue**: CORS errors
- Update `ALLOWED_ORIGINS` in environment variables
- Ensure proper origin format (include protocol)

## License

ISC

## Support

For issues and questions:
- GitHub Issues: https://github.com/SahanaNagaraju/news-agent/issues
- Documentation: See deployment guide in `deployment/` folder

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Changelog

### Version 1.0.0 (Initial Release)
- Python/FastAPI implementation
- Newdata.io integration
- RESTful API endpoints
- Auto-generated API documentation
- Render and BTP deployment support
- Health monitoring
- Error handling and logging
- Pydantic validation
- Async/await support
