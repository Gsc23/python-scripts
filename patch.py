import requests
import time

BATCH_SIZE = 20 
headers = {
    "Authorization": "",
    "Content-Type": "application/json"
}

IDS_FILE = "ids.txt"

roles = []

def read_ids():
    with open(IDS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def save_ids(ids):
    
    with open(IDS_FILE, "w") as f:
        for id in ids:
            f.write(id + "\n")

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def send_requests():
    ids = read_ids()
    remaining = ids.copy()

    for _id in ids:
        payload = {
            "rolesIds": roles
        }
        url = f"http://localhost:8080/v1/users/{_id}"

        try:
            resp = requests.patch(url, json=payload, headers=headers)
            if resp.ok:
                print(f"✅ ID {_id} enviado com sucesso!")
                remaining.remove(_id)
            else:
                print(f"❌ ID {_id} falhou: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"⚠️ ID {_id} deu erro: {e}")

        save_ids(remaining)
        time.sleep(1)

if __name__ == "__main__":
    send_requests()
