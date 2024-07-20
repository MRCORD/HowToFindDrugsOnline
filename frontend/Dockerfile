# Use the Python 3.10 slim-buster image as the base image
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /frontend

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install -U pip && pip install -r requirements.txt

# Copy the entire app directory to the working directory
COPY app/ app/

# Expose port 8501 to allow external connections
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app/main.py"]