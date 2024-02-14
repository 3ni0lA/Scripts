import requests
import os
import pymysql
from datetime import datetime

# Retrieve Go-Mailer API Key from environment variable
api_key = os.environ.get("API_KEY")

# Check if the API key is set
if api_key is None:
    print("Go-Mailer API Key environment variable is not set. Make sure to set it before running the script.")
    exit(1)
    
api_url = 'YOUR URL'

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# Retrieve database credentials from environment variables
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")

# Check if all database credentials are set
if None in (db_host, db_user, db_password, db_name):
    print("One or more database credentials environment variables are not set. Make sure to set them before running the script.")
    exit(1)


# MariaDB Database Connection
db = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,

)
# FAILED LOGIN QUERY LINE
data = {
    "template_code": "ALERT",
    "recipient_email": "ops@go-mailer.com",
    "data": {
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "subject": "Failed login attempts",
        "message":  "There have been failed login attempts within a short period.",
    }

}


def check_failed_login_attempts():
    max_attempts = 3
    try:
        cursor = db.cursor()
        query = """
            SELECT COUNT(*) FROM failed_logins
            WHERE timestamp >= NOW() - INTERVAL 5 MINUTE ;
        """
        cursor.execute(query)
        count_failed_attempts = cursor.fetchone()[0]
        cursor.close()

        if count_failed_attempts > max_attempts:
            print("There have been failed login attempts failed login attempts from IP address within a short period, alert sys admin")

    except Exception as e:
        print(
            f"An error occurred while checking failed login attempts: {str(e)}")
    db.close()

response = requests.post(api_url, json=data, headers=headers)

if response.status_code == 200:
    print("Email sent successfully")
    print("Response content:", response.text)  # Print the response content

    # Call the function to check failed login attempts
    check_failed_login_attempts()
   
else:
    print(
        f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")
