FROM python:3
RUN pip install --no-cache-dir boto3
COPY consumer consumer
COPY main.py main.py
CMD ["python", "main.py", "-r", "sqs", "-ss", "s3"]