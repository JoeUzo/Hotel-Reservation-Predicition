FROM python:3.12-alpine3.20

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update && \
    apk add --no-cache libgomp

COPY . .

RUN pip install --no-cache-dir -e .

RUN python pipeline/training_pipeline.py 

EXPOSE 5000

CMD ["python", "app.py"]