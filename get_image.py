import requests

url = "https://thispersondoesnotexist.com"
headers = {"User-Agent": "Mozilla/5.0"}

print("Downloading an AI face for testing...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("test_face.jpg", "wb") as f:
        f.write(response.content)
    print("Success! Look at your left sidebar, 'test_face.jpg' is now there.")
else:
    print("Failed to download. Status code:", response.status_code)
    