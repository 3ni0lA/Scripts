import requests
import os
import pymysql
from datetime import datetime

# Go-Mailer API Key
api_key = os.environ.get("API_KEY")

# Check if the API key is set
if api_key is None:
    print("Go-Mailer API Key environment variable is not set. Make sure to set it before running the script.")
    exit(1)
    
api_url = 'API_URL'

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
    database=db_name

)


data = {
    "template_code": "ALERT",
    "recipient_email": "example@go-mailer.com",
    "data": {
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "subject": "Suspicious activity",
        "message":  "Suspicious database activity detected. Immediate investigation required.",
    }

}
        
def log_security_event(ip_address, event_type):
    try:
        cursor = db.cursor()
        query = """
            INSERT INTO security_events (event_timestamp, ip_address, event_type)
            VALUES (NOW(), %s, %s);
        """
        cursor.execute(query, (ip_address, event_type))
        db.commit()
        cursor.close()
    except Exception as e:
        print(f"Security event logging error: {str(e)}")

def check_security_events():
    max_events = 2
    try:
        cursor = db.cursor()
        query = """
            SELECT COUNT(*) FROM security_events
            WHERE timestamp >= NOW() - INTERVAL 1 HOUR
            AND event_type = 'Unauthorized Login';
        """

        cursor.execute(query)
        count_security_events = cursor.fetchone()[0]
        cursor.close()

        if count_security_events > max_events:
            print("Suspicious database activity.")
            # Implement source blocking logic here if needed

    except Exception as e:
        print(f"Security event error: {str(e)}")     

    db.close()

response = requests.post(api_url, json=data, headers=headers)

if response.status_code == 200:
    print("Email sent successfully")
    print("Response content:", response.text)  # Print the response content

    # Call the function to check Unauthorised login attempts
   
    log_security_event("unknown", "Unauthorized Login")

else:
    print(
        f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")
