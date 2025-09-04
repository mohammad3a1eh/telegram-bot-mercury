# Use official Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Command to run your bot
CMD ["python", "mercury.py"]
