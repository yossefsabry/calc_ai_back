dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8900
run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8900

docker-build:
	docker build -t power-calc-ai-backend .

docker-run:
	docker run -e GEMINI_API_KEY=$$GEMINI_API_KEY -p 8900:8900 power-calc-ai-backend

install:
	uv pip install -r requirements.txt

