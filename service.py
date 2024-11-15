import requests
import os
import time
import signal
import traceback
import qbittorrentapi


def main():
    print("Starting")

    sleep_time = int(os.environ["SECONDS_BETWEEN_UPDATE"])

    gluetun_url = "http://" + os.environ["GLUETUN_ADDRESS"] + ":8000/v1/openvpn/portforwarded"
    gluetun_headers = {"X-API-Key": os.environ["GLUETUN_API_KEY"]}

    conn_info = dict(
        host=os.environ["QBIT_ADDRESS"],
        port=os.environ["QBIT_PORT"],
        username=os.environ["QBIT_USERNAME"],
        password=os.environ["QBIT_PASSWORD"],
    )
    qbt_client = qbittorrentapi.Client(**conn_info)

    while True:
        time.sleep(sleep_time)
        try:
            r = requests.get(gluetun_url, headers=gluetun_headers)
            r_json = r.json()
            vpn_port = r_json["port"]

            #print("VPN forwarded port: " + str(vpn_port))
        except Exception as e:
            print("Error contacting gluetun: " + str(e))
            continue
        try:
            qbt_client.auth_log_in()

        except qbittorrentapi.LoginFailed as e:
            print(e)
            continue
        
        try:
            qbit_port = qbt_client.app_preferences().get("listen_port")
            #print("Qbittorrent is listening on:", qbit_port)
            if qbit_port != vpn_port:
                print("Wrong port defined, changing!")
                qbt_client.app_set_preferences({"listen_port": vpn_port})
                print("Listening port changed to:", vpn_port)
            else:
                print("Port matches vpn")
        except:
            traceback.print_exception()
            continue
            
        try:
            qbt_client.auth_log_out()
        except:
            traceback.print_exception()
            continue

def handler(signum, frame):
    print('Exiting')
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handler)
    main()

