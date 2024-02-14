import requests
import json
import subprocess
from datetime import datetime
import os

headers = {
    "Content-Type": "application/json",
}

# Database credentials
# Retrieve environment variables
slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
db_name = os.environ.get("DB_NAME")

if slack_webhook_url is None:
    print("Slack Webhook URL environment variable is not set. Make sure to set it before running the script.")
    exit(1)

# Generate a timestamp
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

# Specify the target directory with the timestamp
target_dir = f'/var/backups/mysql/mariadb_backup_emaillogs_{timestamp}'


# Prepare Slack notification data
def send_slack_notification(text, username, icon_emoji):
    data = {
        "text": text,
        "username": username,
        "icon_emoji": icon_emoji,
    }
    response = requests.post(slack_webhook_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Notification sent to Slack.")
    else:
        print(f"Failed to send notification to Slack: {response.status_code}")
# Run the mariabackup command with the updated target directory
try:
    subprocess.run(['mariabackup', '--backup', '--target-dir=' + target_dir, '--databases=logs'])
    print(f"Backup successful. Backup file saved to {target_dir}")
    send_slack_notification("Database backup is successful.", "Demo App", ":white_check_mark:")
except subprocess.CalledProcessError as e:
    print(f"Backup failed: {e}")
    send_slack_notification("Scheduled database backup has failed. Please investigate and resolve the issue.", "Demo App", ":exclamation:")
