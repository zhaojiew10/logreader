FROM python:3.9.18-alpine3.18
WORKDIR /app
ADD ./ /app
CMD ["python", "/app/main.py"]