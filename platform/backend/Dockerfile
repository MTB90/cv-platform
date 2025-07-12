FROM python:3.12

WORKDIR /src
ENV PYTHONPATH /src

# Copy only the requirements.txt first to leverage Docker cache more efficiently
COPY requirements.txt /src/requirements.txt

# Install dependencies separately to take advantage of Docker layer caching
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /src/requirements.txt

COPY ./app /src
CMD ["uvicorn", "--host", "0.0.0.0", "main:app",  "--port", "8000", "--workers", "4", "--reload"]
