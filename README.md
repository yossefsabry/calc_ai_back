# Power Calc AI Backend

This is a FastAPI backend for analyzing mathematical expressions, equations, and graphical math problems from images using Google Gemini AI.

## Features
- Analyze images with math expressions, equations, or graphical problems
- Handles variable assignment and substitution
- Robust error handling and logging
- Concurrent request handling
- Health check endpoint
- Dockerized for easy deployment
- Environment variable configuration

## Requirements
- Python 3.8+
- Google Gemini API key

## Setup
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd calc_ai_back
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Gemini API key in `constants.py` or as an environment variable:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```
4. Run the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Docker
1. Build the Docker image:
   ```bash
   docker build -t power-calc-ai-backend .
   ```
2. Run the container:
   ```bash
   docker run -e GEMINI_API_KEY=your_api_key_here -p 8000:8000 power-calc-ai-backend
   ```

## API Usage
### POST /calculate
Analyze an image with math expressions.

**Request Body:**
```json
{
  "image": "data:image/png;base64,<base64-data>",
  "dict_of_vars": {"x": 2, "y": 3}
}
```

**Response:**
```json
{
  "message": "Success",
  "data": [
    {"expr": "2 + 2", "result": 4, "assign": false}
  ],
  "status": "success"
}
```

### GET /calculate/health
Health check endpoint.

**Response:**
```json
{"status": "ok"}
```

## Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GEMINI_TIMEOUT`: Timeout for Gemini API call in seconds (default: 30)

## License
MIT
