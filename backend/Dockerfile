# # Use the Python 3.10 slim-buster image as the base image
# FROM python:3.10-slim-buster 
# #AS bas

# # Set the working directory inside the container
# WORKDIR /backend

# # Copy the requirements.txt file to the working directory
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install -U pip && pip install -r requirements.txt

# # Copy the application code to the working directory
# COPY app app

# EXPOSE 8000

# # Command to run the ASGI app
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# Use the Python 3.10 slim-buster image as the base image
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /backend

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install -U pip && pip install -r requirements.txt

# Copy the entire contents of the FastAPI_Backend directory to the working directory
COPY . .

# Grant execute permission to the initializer script
RUN chmod +x initializer.sh

# Expose port 8000 to allow external connections
EXPOSE 8000

# Command to run the initializer script
CMD ["/bin/bash", "initializer.sh"]

#CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

LABEL org.opencontainers.image.source https://github.com/mrcord/howtofinddrugsonline