FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY market_sage_pro/ /app/market_sage_pro/
COPY config.yaml.example /app/
CMD ["python", "-m", "market_sage_pro.scheduler.jobs"]
