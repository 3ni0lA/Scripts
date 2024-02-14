import requests
import pymysql
from datetime import datetime

# Go-Mailer API Key
api_key = 'API_KEY'
api_url = 'API_URL'
  
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
 
 # MariaDB Database Connection
db = pymysql.connect(
    host="DB_HOST,
    user="DB_USER",
    password="DB_PASSWD",
    database="DB_NAME"
    
)
data = {
"template_code":"ALERT",
"recipient_email":"example@go-mailer.com",
"data" :{
   "current_date":"2023-09-20"
}

}
response = requests.post(api_url, json=data, headers=headers )

if response.status_code == 200:
    print("Email sent successfully")
    print("Response content:", response.text)  # Print the response content
else:
    print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")
    db.close()
