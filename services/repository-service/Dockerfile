FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# Install CPU-only PyTorch to avoid unnecessary NVIDIA CUDA libraries.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
       --index-url https://download.pytorch.org/whl/cpu \
       torch==2.6.0+cpu \
    && pip install --no-cache-dir -r requirements.txt


COPY . .

RUN useradd --create-home --home-dir /home/appuser --shell /usr/sbin/nologin appuser     && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
