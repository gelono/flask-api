import requests


# url = 'http://127.0.0.1:5000/hello'
url = 'https://vm5043127.43ssd.had.wf:5000/hello'
# token = 'skdjgh14dfjbl246dklwjgqsdfvbsfb2r52'
token = 'uaysdgfuqcyk13rkuahcvuy3115135'

headers = {'Authorization': 'Bearer ' + token}
response = requests.post(url, headers=headers, verify='vm5043127.43ssd.had.wf-crt.pem')

if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code)
    print("Response:", response.json())
