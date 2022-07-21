FROM python:3.9-slim

WORKDIR /app/client
COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

COPY pyclient pyclient

CMD ["python", "pyclient/client.py"]
