FROM python:3.12 AS builder

# Copy only the requirements.txt first to leverage Docker cache more efficiently
COPY requirements.txt /src/requirements.txt

# Install dependencies separately to take advantage of Docker layer caching
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /src/requirements.txt


FROM python:3.12-slim

WORKDIR /src
ENV PYTHONPATH=/src

# Copy dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./app /src
CMD ["uvicorn", "--host", "0.0.0.0", "main:app",  "--port", "8000", "--workers", "4"]
