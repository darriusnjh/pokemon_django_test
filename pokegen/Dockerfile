FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

# Install build dependencies (for Pillow, psycopg2, etc.)
RUN apk add --no-cache gcc musl-dev libffi-dev jpeg-dev zlib-dev

WORKDIR /pokegen

# Copy requirements and install them
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose port 8000
EXPOSE 8080

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
