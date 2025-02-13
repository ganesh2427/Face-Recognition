import json
import mysql.connector
import requests

def addface(file_url):
    url = "https://api.edenai.run/v2/image/face_recognition/add_face"

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

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()   
        return response.json()  # ✅ Return JSON instead of text
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None  # Return None if request fails

# ✅ Load User Data from input.json
try:
    with open("input.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("❌ Error: input.json file not found!")
    exit()

# ✅ Function to Insert Data into MySQL
def insert_data(data):
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Pirates@1947",  # Change this to your actual password
            database="new"
        )
        if conn.is_connected():
            print("✅ Connected to MySQL database")
    except mysql.connector.Error as e:
        print(f"❌ MySQL Connection Error: {e}")
        return

    cur = conn.cursor()

    for item in data.get("user_info", []):
        mail_id = item.get("mail_id")
        name = item.get("name")
        image_url = item.get("image_url")

        # ✅ Call API to get face ID
        response = addface(image_url)
        if response is None:
            print(f"⚠️ Skipping {mail_id} due to API error")
            continue

        # ✅ Extract Face IDs
        face_ids = response.get("amazon", {}).get("face_ids", [])
        face_id = ", ".join(face_ids) if face_ids else "No Face ID"
        print(f"👤 Face ID for {mail_id}: {face_id}")

        # ✅ Insert into MySQL
        try:
            sql_insert = "INSERT INTO UserDetails (MAIL_ID, NAME, IMAGE_URL, SERVER_ID) VALUES (%s, %s, %s, %s)"
            cur.execute(sql_insert, (mail_id, name, image_url, face_id))
            print(f"✅ Inserted: {mail_id} | {name} | {face_id}")
        except mysql.connector.IntegrityError:
            print(f"⚠️ Duplicate entry for {mail_id}, Skipping...")
            continue

    # ✅ Commit and close connection
    conn.commit()
    cur.close()
    conn.close()
    print("🎉 All data processed successfully!")

# ✅ Run the function
insert_data(data)
