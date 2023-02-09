FROM python:latest
RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip
COPY .. /binanse_futures_monitoring/
WORKDIR /binanse_futures_monitoring
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]
