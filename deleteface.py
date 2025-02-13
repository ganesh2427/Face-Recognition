# import requests

# url = "https://api.edenai.run/v2/image/face_recognition/delete_face"

# payload = {
#     "response_as_dict": True,
#     "attributes_as_list": False,
#     "show_original_response": False,
#     "providers": "amazon",
#     "face_id": "fcce2021-2233-4176-8aaf-9e051b2ed479"
# }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTQ1NDgyODAtNjNmZC00MmEzLWI2M2QtNDI5YTI4ZDliNTc2IiwidHlwZSI6ImFwaV90b2tlbiJ9.W2qckEzb4fsWyJfyL3mRHZjQeg-l81hMI87t2-82yvk"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)

 
import json
import mysql.connector
import requests

import requests
def deleteface(face_id):
    url = "https://api.edenai.run/v2/image/face_recognition/delete_face"

    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "providers": "amazon",
        "face_id": face_id
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTQ1NDgyODAtNjNmZC00MmEzLWI2M2QtNDI5YTI4ZDliNTc2IiwidHlwZSI6ImFwaV90b2tlbiJ9.W2qckEzb4fsWyJfyL3mRHZjQeg-l81hMI87t2-82yvk"
    }

    response = requests.post(url, json=payload, headers=headers)
    

    return response.text


try:
    with open("delete.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("❌ Error: input.json file not found!")
    exit()

def delete_data(data):
# Connect to MySQL database
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
        mail_id = item['mail_id']
        # sql_select = "SELECT SERVER_ID FROM UserDetails WHERE MAIL_ID = %s"
        # response = deleteface(sql_select)
        # print("Face IDs deleted from API:", )
        
        try:
            sql_select = "SELECT SERVER_ID FROM UserDetails WHERE MAIL_ID = %s"
            cur.execute(sql_select, (mail_id,))
            face_id = cur.fetchone()[0]
            
            print("Face IDs deleted from API:", face_id)
            response = deleteface(face_id)
            print("Face IDs deleted from API:", response)
            
            sql_delete = "DELETE FROM UserDetails WHERE MAIL_ID = %s"
            cur.execute(sql_delete, (mail_id,))
            print(cur.rowcount, "row(s) deleted")
        except mysql.connector.Error as e:
            print("An error occurred:", e)
            continue    

    conn.commit()
    cur.close()
    conn.close()

delete_data(data)
