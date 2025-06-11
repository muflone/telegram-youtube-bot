FROM python:3.12.8-alpine3.21

WORKDIR /app
COPY . .
RUN python3 -m pip install -r requirements.txt

USER nobody:nobody
CMD ["python3", "./main.py"]
