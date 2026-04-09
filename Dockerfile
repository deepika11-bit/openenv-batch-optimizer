FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --no-deps openenv-core
RUN pip install --no-cache-dir fastapi uvicorn pydantic numpy python-dotenv openai

CMD ["python", "inference.py"]