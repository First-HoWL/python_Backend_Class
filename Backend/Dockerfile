# Use an official Python runtime as the base image
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python output is sent directly to terminal
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (optional if using Django staticfiles)
RUN python manage.py collectstatic --noinput

# Expose application port
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]