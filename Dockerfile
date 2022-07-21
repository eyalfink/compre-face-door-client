FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/client
COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

COPY pyclient pyclient

CMD ["python", "pyclient/client.py"]
