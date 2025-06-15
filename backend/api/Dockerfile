FROM python:3.11-slim-buster

# Set working directory
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker cache
COPY ./api/requirements.txt requirements.txt

# Install requirements
RUN pip3 install -r requirements.txt

# Copy the application
COPY ./api/ ./
# COPY ./api/models /models

# Expose the port for the app to run
EXPOSE 80

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "app:app", "--reload"]