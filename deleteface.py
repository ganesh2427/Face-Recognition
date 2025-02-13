import requests

url = "https://api.edenai.run/v2/image/face_recognition/delete_face"

payload = {
    "response_as_dict": True,
    "attributes_as_list": False,
    "show_original_response": False,
    "providers": "amazon",
    "face_id": "7bde4803-d2c3-4441-b672-3f0155091361"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTQ1NDgyODAtNjNmZC00MmEzLWI2M2QtNDI5YTI4ZDliNTc2IiwidHlwZSI6ImFwaV90b2tlbiJ9.W2qckEzb4fsWyJfyL3mRHZjQeg-l81hMI87t2-82yvk"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

 