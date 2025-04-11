import os
import requests

ca_dir = "aiven_ca"
os.makedirs(ca_dir, exist_ok=True)

ca_path = os.path.join(ca_dir, "ca.pem")
ca_url = "https://aiven.io/ca.pem"

print("🔐 CA 인증서 다운로드 중...")

response = requests.get(ca_url)
with open(ca_path, "wb") as f:
    f.write(response.content)

print(f"✅ 저장 완료: {ca_path}")
print("🔐 CA 인증서 다운로드 완료")