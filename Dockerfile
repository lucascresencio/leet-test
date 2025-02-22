FROM python:3.9.21-alpine3.21

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 5050

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]