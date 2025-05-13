# Use the official Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main.py file to the container
COPY main.py .
COPY src ./src

# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Start the FastAPI app
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]