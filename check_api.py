import requests


# url = 'http://127.0.0.1:5000/hello'
url = 'http://45.132.105.156:5000/hello'
# token = 'skdjgh14dfjbl246dklwjgqsdfvbsfb2r52'
token = 'uaysdgfuqcyk13rkuahcvuy3115135'

headers = {'Authorization': 'Bearer ' + token}
response = requests.post(url, headers=headers)

if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code)
    print("Response:", response.json())
