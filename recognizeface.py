# import requests

# url = "https://api.edenai.run/v2/image/face_recognition/recognize"

# payload = {
#     "response_as_dict": True,
#     "attributes_as_list": False,
#     "show_original_response": False,
#     "providers": "amazon",
#     "file_url": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Narendra_modi.jpg"
#     #"file_url": "https://upload.wikimedia.org/wikipedia/commons/5/56/Rahul_Gandhi_%28full%29.jpg"
# }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTQ1NDgyODAtNjNmZC00MmEzLWI2M2QtNDI5YTI4ZDliNTc2IiwidHlwZSI6ImFwaV90b2tlbiJ9.W2qckEzb4fsWyJfyL3mRHZjQeg-l81hMI87t2-82yvk"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)

# # import requests

# # def recognizeface(file_url)
# #     url = "https://api.edenai.run/v2/image/face_recognition/recognize"

# #     payload = {
# #         "response_as_dict": True,
# #         "attributes_as_list": False,
# #         "show_original_response": False,
# #         "providers": "amazon",
# #         "file_url": "https://upload.wikimedia.org/wikipedia/commons/b/be/Indian_Prime_Minister_Narendra_Modi.jpg"
# #     }
# #     headers = {
# #         "accept": "application/json",
# #         "content-type": "application/json",
# #         "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTQ1NDgyODAtNjNmZC00MmEzLWI2M2QtNDI5YTI4ZDliNTc2IiwidHlwZSI6ImFwaV90b2tlbiJ9.W2qckEzb4fsWyJfyL3mRHZjQeg-l81hMI87t2-82yvk"
# #     }

# #     response = requests.post(url, json=payload, headers=headers)

# #     print(response.text)



import json
import mysql.connector
import requests

def recognizeface(file_url):
    url = "https://api.edenai.run/v2/image/face_recognition/recognize"

    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "providers": "amazon",
        "file_url": file_url
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTQ1NDgyODAtNjNmZC00MmEzLWI2M2QtNDI5YTI4ZDliNTc2IiwidHlwZSI6ImFwaV90b2tlbiJ9.W2qckEzb4fsWyJfyL3mRHZjQeg-l81hMI87t2-82yvk"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.ok:
        items = response.json()["amazon"]["items"]
        if items:  # Check if items list is not empty
            return items[0]["face_id"]
    return None


try:
    with open("recognizeface.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("❌ Error: input.json file not found!")
    exit()

# Connect to MySQL database
def recognize(data):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Pirates@1947",  # Change this to your actual password
            database="new"
        )
        if conn.is_connected():
            print("Connected to MySQL database")
    except Exception as e:
        print("Error: Unable to connect to MySQL database")

    cur = conn.cursor()

    for item in data['user_info']:
        image_url = item['image_url']
        mail_id = item['mail_id']

        face_id = recognizeface(image_url)
        if face_id:
            print("Face ID:", face_id)
            try:
                sql_select = "SELECT MAIL_ID, NAME FROM UserDetails WHERE SERVER_ID = %s"
                cur.execute(sql_select, (face_id,))
                result = cur.fetchone()

                if result:
                    mail_id = result[0]
                    name = result[1]
                    print("Mail ID:", mail_id)
                    print("Name:", name)
                else:
                    print("No record found for the given face ID")
            except mysql.connector.Error as e:
                print("Error occurred while executing the SQL query:", e)

        else:
            print("no image matches")
        

    conn.commit()
    cur.close()
    conn.close()

recognize(data)