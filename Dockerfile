FROM python:3.10-slim

WORKDIR /app

COPY . .

# ✅ install everything properly
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ✅ start server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]