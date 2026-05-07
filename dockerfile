FROM python:3.12-slim

WORKDIR /app

#install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

#create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/opt/venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
