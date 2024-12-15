FROM python:3.9.18-alpine3.18
WORKDIR /app/logreader
ADD ./main.py /app/main.py
CMD ["python", "../main.py"]
