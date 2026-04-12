FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --no-deps openenv-core
RUN pip install --no-cache-dir fastapi uvicorn pydantic numpy python-dotenv openai

CMD sh -c "uvicorn server.app:app --host 0.0.0.0 --port 7860 & python inference.py"