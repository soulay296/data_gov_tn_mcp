FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir --timeout 120 --retries 10 .
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
