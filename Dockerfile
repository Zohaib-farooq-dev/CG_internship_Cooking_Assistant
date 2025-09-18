FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ---

# Stage 2: Final Stage (for the application)
FROM python:3.11-slim

# Create a non-root user for security
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser
USER appuser
WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy your application code
COPY . .

# Run the application
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]