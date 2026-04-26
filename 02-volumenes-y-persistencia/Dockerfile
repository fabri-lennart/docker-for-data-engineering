# Use the slim Python 3.8 image
FROM python:3.12-slim
# Set the working directory
WORKDIR /app
# Copy application files
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application
COPY pipeline_v2.py .
# Run the application
CMD ["python", "pipeline_v2.py"]
