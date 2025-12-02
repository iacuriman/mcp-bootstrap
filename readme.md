# MCP Bootstrap - Model Context Protocol Server

A modular FastAPI-based server that implements the Model Context Protocol (MCP) for exposing tools to AI models. This server allows you to easily add and manage tools that can be discovered and executed by AI assistants.

## Features

- **Modular Architecture**: Easily add new tools by creating simple Python modules
- **MCP Protocol**: Implements the Model Context Protocol for tool discovery and execution
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **Real Weather Data**: Example tool that fetches real-time weather using Open-Meteo API

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

### Step 1: Clone or Navigate to the Project

```bash
cd /path/to/mcp-bootstrap
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

### Start the Server

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reload on code changes, which is useful during development.

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The server will be available at: **http://localhost:8000**

### Stop the Server

Press `CTRL+C` in the terminal where the server is running.

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Usage

### Endpoint

**POST** `/mcp`

### Request Format

The server accepts two types of requests:

#### 1. Discovery Request

Discover available tools:

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"verb": "discovery"}'
```

**Response:**
```json
{
  "tools": [
    {
      "name": "get_weather",
      "description": "Get the weather for a given location",
      "parameters": [
        {
          "name": "location",
          "type": "string"
        }
      ]
    }
  ],
  "result": null
}
```

#### 2. Execute Request

Execute a tool:

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"verb": "execute", "tool_name": "get_weather", "arguments": {"location": "Madrid"}}'
```

**Response:**
```json
{
  "tools": null,
  "result": "Current weather in Madrid, Spain: 18°C, partly cloudy, humidity 65%, wind 12 km/h"
}
```

### Example: Get Weather for Different Locations

```bash
# Get weather for Murcia, Spain
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"verb": "execute", "tool_name": "get_weather", "arguments": {"location": "Murcia"}}'

# Get weather for New York
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"verb": "execute", "tool_name": "get_weather", "arguments": {"location": "New York"}}'

# Get weather for Paris
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"verb": "execute", "tool_name": "get_weather", "arguments": {"location": "Paris"}}'
```

## Project Structure

```
mcp-bootstrap/
├── main.py              # FastAPI application and route handlers
├── models.py            # Pydantic models for requests/responses
├── toolGetWeather.py    # Example weather tool implementation
├── requirements.txt     # Python dependencies
├── readme.md           # This file
├── add-tool.md         # Guide for adding new tools
└── venv/               # Virtual environment (created during setup)
```

## Adding New Tools

To add new tools to this modular application, see **[add-tool.md](add-tool.md)** for detailed instructions.

## Error Handling

The server returns appropriate HTTP status codes:

- **200 OK**: Successful request
- **400 Bad Request**: Invalid verb, missing tool, or invalid arguments
- **500 Internal Server Error**: Error executing tool

## Development

### Auto-reload

The server runs with `--reload` flag by default, so any changes to the code will automatically restart the server.

### Testing

You can test the API using:
- `curl` commands (as shown above)
- The interactive Swagger UI at http://localhost:8000/docs
- Any HTTP client (Postman, Insomnia, etc.)

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, you can specify a different port:

```bash
uvicorn main:app --reload --port 8001
```

### Module Import Errors

Make sure you're running the server from the project root directory and that your virtual environment is activated.

### Dependencies Not Found

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

## License

This project is open source and available for use.
