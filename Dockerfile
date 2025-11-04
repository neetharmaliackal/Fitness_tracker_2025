# Use Python 3.11 as base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files into container
COPY . .

# Expose port 8000 (Django default)
EXPOSE 8000

# Command to run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
