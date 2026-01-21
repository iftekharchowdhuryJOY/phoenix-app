FROM python:3.9-slim

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]