# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the local directory into the container at /app
COPY . /app

# Install any dependencies specified in setup.py
RUN pip install .

# Specify the command to run your Python script
CMD ["python", "src/log_analyzer.py", "data/inputs/access.log", "data/outputs/result.json", "--mfip", "--lfip", "--eps", "--bytes"]


