FROM python:slim
WORKDIR /app
ADD ./ /app
CMD ["python", "/app/main.py"]