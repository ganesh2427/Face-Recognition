# import requests

# url = "https://api.edenai.run/v2/image/face_recognition/list_faces?attributes_as_list=false&providers=amazon&response_as_dict=true&show_original_response=false"

# headers = {
#     "accept": "application/json",
#     "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTQ1NDgyODAtNjNmZC00MmEzLWI2M2QtNDI5YTI4ZDliNTc2IiwidHlwZSI6ImFwaV90b2tlbiJ9.W2qckEzb4fsWyJfyL3mRHZjQeg-l81hMI87t2-82yvk"
# }

# response = requests.get(url, headers=headers)

# print(response.text)

import requests
import json
import mysql.connector

def get_face_data():
    url = "https://api.edenai.run/v2/image/face_recognition/list_faces"
    params = {
        "attributes_as_list": "false",
        "providers": "amazon",
        "response_as_dict": "true",
        "show_original_response": "false"
    }
    
    headers = {
        "accept": "application/json",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTQ1NDgyODAtNjNmZC00MmEzLWI2M2QtNDI5YTI4ZDliNTc2IiwidHlwZSI6ImFwaV90b2tlbiJ9.W2qckEzb4fsWyJfyL3mRHZjQeg-l81hMI87t2-82yvk"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Pretty-print the result
        print(json.dumps(data, indent=4))
        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None

def fetch_database_data():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Pirates@1947",  # Change this to your actual password
            database="new"
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM UserDetails")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        if rows:
            print(" | ".join(columns))
            print("-" * 50)
            for row in rows:
                print(" | ".join(str(item) if item is not None else "NULL" for item in row))
        else:
            print("No data available in the table.")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")

# Run the functions
get_face_data()
fetch_database_data()

