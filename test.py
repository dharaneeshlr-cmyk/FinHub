
import requests


resp = requests.get("http://127.0.0.1:5000/api/sync")


# access_token = "2I0k3uqsZ0viadsQGcxLxcjl6J95Jz2V"  # paste current token
# api_key = "hi30f0cztcpm37av"

# headers = {
#     "X-Kite-Version": "3",
#     "Authorization": f"token {api_key}:{access_token}"
# }

# resp = requests.get("https://api.kite.trade/portfolio/holdings", headers=headers)
print(resp.status_code)
print(resp.json())