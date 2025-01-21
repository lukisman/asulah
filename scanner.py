
import requests
import json
from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = "http://elasticsearch:9200"

# Inisialisasi Elasticsearch
es = Elasticsearch(ELASTICSEARCH_URL)

# Fungsi untuk cek file sftp.json
def check_sftp_config(ip_list):
    found = []
    for ip in ip_list:
        url = f"http://{ip}:22/.vscode/sftp.json"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"[+] Found: {url}")
                found.append({"ip": ip, "url": url})
            else:
                print(f"[-] Not Found: {url}")
        except requests.exceptions.RequestException:
            print(f"[!] Error connecting to {ip}")
    return found

# Load hasil Masscan
def load_masscan_results(file):
    with open(file, "r") as f:
        data = json.load(f)
        return [item["ip"] for item in data["hosts"]]

# Simpan hasil ke Elasticsearch
def index_results(results):
    for item in results:
        es.index(index="vscode_sftp", body=item)

if __name__ == "__main__":
    ip_list = ["127.0.0.1", "192.168.0.1"]  # Ganti dengan hasil Masscan
    results = check_sftp_config(ip_list)
    index_results(results)
