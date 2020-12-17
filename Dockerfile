FROM python:3

COPY api.py .

COPY app.py .

COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 80/tcp

ENTRYPOINT ["python3", "app.py"]

