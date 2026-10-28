FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY event_helper.py index.html server.py ./

EXPOSE 8000

CMD ["python", "server.py"]
