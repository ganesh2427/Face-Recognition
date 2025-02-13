import requests

url = "https://api.edenai.run/v2/image/face_recognition/list_faces?attributes_as_list=false&providers=amazon&response_as_dict=true&show_original_response=false"

headers = {
    "accept": "application/json",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTQ1NDgyODAtNjNmZC00MmEzLWI2M2QtNDI5YTI4ZDliNTc2IiwidHlwZSI6ImFwaV90b2tlbiJ9.W2qckEzb4fsWyJfyL3mRHZjQeg-l81hMI87t2-82yvk"
}

response = requests.get(url, headers=headers)

print(response.text)