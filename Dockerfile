FROM python:bookworm

WORKDIR /app
COPY service.py service.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV SECONDS_BETWEEN_UPDATE=3600
ENV GLUETUN_ADDRESS=gluetun
ENV QBIT_ADDRESS=qbittorrent
ENV QBIT_PORT=8080
ENV QBIT_USERNAME=admin
ENV QBIT_PASSWORD=password

#ENTRYPOINT [ "bash" ]
ENTRYPOINT ["python", "-u", "/app/service.py" ]