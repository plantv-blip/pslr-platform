FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create database directory
RUN mkdir -p /app/instance

# Expose port
EXPOSE 5000

# Set environment
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Run migrations and start server
CMD ["sh", "-c", "flask db upgrade && gunicorn app:app --config gunicorn.conf.py"]
