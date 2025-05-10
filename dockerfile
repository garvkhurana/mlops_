
FROM python:3.13-slim	

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

CMD ["python", "app.py"]






