# 1) Base image choose karo (Linux + Python installed)
FROM python:3.11.9-slim

# 2) Container ke andar ka working directory set karo
WORKDIR /app

# 3) Dependencies copy karo (requirements.txt) 
COPY requirements.txt .

# 4) Dependencies install karo
RUN pip install --no-cache-dir -r requirements.txt

# 5) Apna code copy karo container ke andar
COPY . .

# 6) FastAPI ko uvicorn ke saath run karne ka command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]