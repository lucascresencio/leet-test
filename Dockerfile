FROM python:3.9.21-alpine3.21

# Set working directory
WORKDIR /app

# Copy the application code
COPY . .

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 5050

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050"]