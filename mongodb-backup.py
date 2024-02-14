import subprocess
import datetime
import os

# Get credentials from environment variables
mongodb_host = os.environ.get('MONGODB_HOST')
mongodb_port = os.environ.get('MONGODB_PORT')
mongodb_db_name = os.environ.get('MONGODB_DB_NAME')
mongodb_user = os.environ.get('MONGODB_USER')
mongodb_password = os.environ.get('MONGODB_PASSWORD')

if not (mongodb_host and mongodb_port and mongodb_db_name and mongodb_user and mongodb_password):
    print("MongoDB environment variables are not set. Make sure to set them before running the script.")
    exit(1)

# Backup directory
backup_dir = '/var/backups/mongodb/'

# Timestamp for the backup
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Backup file name
backup_file = f'{timestamp}_backup.gz'

# Create a backup of the MongoDB database
backup_command =  f'mongodump --host {mongodb_host}:{mongodb_port} --db {mongodb_db_name} --username {mongodb_user} --password {mongodb_password} --gzip --archive={os.path.join(backup_dir, backup_file)}'
backup_success = subprocess.call(backup_command, shell=True)


if backup_success == 0:
    print(f"MongoDB backup successful. File: {os.path.join(backup_dir, backup_file)}")
else:
    print("MongoDB backup failed.")


# Push the backup to another server (replace with your SSH command)
remote_server = os.environ.get('REMOTE_SERVER')
remote_backup_dir = os.environ.get('REMOTE_BACKUP_DIR')

if not remote_backup_dir:
    print("Remote backup directory environment variable is not set. Make sure to set it before running the script.")
    exit(1)
    
push_command = f'scp {os.path.join(backup_dir, backup_file)} {remote_server}:{remote_backup_dir}'
push_success = subprocess.call(push_command, shell=True)

if push_success == 0:
    print(f"Backup pushed to remote server successfully.")
else:
    print("Backup push to remote server failed.")


# Clean up old backups (optional)
# Retain backups for N days, and delete older backups
retention_days = 7
cleanup_command = f'find {backup_dir} -name "*.gz" -mtime +{retention_days} -exec rm {{}} \;'
cleanup_success = subprocess.call(cleanup_command, shell=True)

if cleanup_success == 0:
    print("Old backups cleaned up successfully.")
else:
    print("Cleanup of old backups failed.")