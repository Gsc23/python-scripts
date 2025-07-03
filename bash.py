import requests
import time

API_URL = "http://localhost:8080/v1/bulkUsers"
BATCH_SIZE = 20 
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTE2MzQ1MzgsImlzcyI6ImRpZ2l0YWwtcmJhYyIsInN1YiI6Im9pbHNwaWxsLWRldiJ9.xQZsn_a1k6a1lo3mBuV48_5a3JKhC0UoGDdTW-hYVr0",
    "Content-Type": "application/json"
}

EMAILS_FILE = "emails.txt"

organizations_ids = []
subscriptions_ids = []
roles = []

def read_emails():
    with open(EMAILS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def save_emails(emails):
    with open(EMAILS_FILE, "w") as f:
        for email in emails:
            f.write(email + "\n")

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def send_batches():
    emails = read_emails()
    remaining = emails.copy()

    for idx, batch in enumerate(chunk_list(emails, BATCH_SIZE), start=1):
        payload = {
            "emails": batch,
            "organizationsIds": organizations_ids,
            "subscriptionsIds": subscriptions_ids,
            "roles": roles
        }

        try:
            resp = requests.post(API_URL, json=payload, headers=headers)
            if resp.ok:
                print(f"✅ Lote {idx} enviado com sucesso! {len(batch)} emails")
                for email in batch:
                    remaining.remove(email)
            else:
                print(f"❌ Lote {idx} falhou: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"⚠️ Lote {idx} deu erro: {e}")

        save_emails(remaining)
        time.sleep(1)

if __name__ == "__main__":
    send_batches()
