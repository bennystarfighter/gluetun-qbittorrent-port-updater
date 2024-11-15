FROM python:bookworm

WORKDIR /app
COPY service.py service.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV SECONDS_BETWEEN_UPDATE=60
ENV GLUETUN_ADDRESS=gluetun
ENV GLUETUN_API_KEY=apikey
ENV QBIT_ADDRESS=qbittorrent
ENV QBIT_PORT=8080
ENV QBIT_USERNAME=admin
ENV QBIT_PASSWORD=password

ENTRYPOINT [ "bash", "-c", "while true; do echo starting script; python /app/service.py; sleep 5; done"]
