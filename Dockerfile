# # 1) Base image choose karo (Linux + Python installed)
# FROM python:3.11.9-slim

# # 2) Container ke andar ka working directory set karo
# WORKDIR /app

# # 3) Dependencies copy karo (requirements.txt) 
# COPY requirements.txt .

# # 4) Dependencies install karo
# RUN pip install --no-cache-dir -r requirements.txt

# # 5) Apna code copy karo container ke andar
# COPY . .

# # 6) FastAPI ko uvicorn ke saath run karne ka command
# CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 1: Builder Stage (for installing dependencies)
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---

# Stage 2: Final Stage (for the application)
FROM python:3.11-slim

# Create a non-root user for security
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser
USER appuser
WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy your application code
COPY . .

# Run the application
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]