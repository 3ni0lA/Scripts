import subprocess
import datetime
import os

# MongoDB settings
mongodb_host = 'localhost'
mongodb_port = '27017'
mongodb_db_name = 'admin'
mongodb_user = 'email'  # Replace with your MongoDB username
mongodb_password = 'password'  # Replace with your MongoDB password

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
remote_server = 'demo@ip_adress'
remote_backup_dir = '/var/backups/mysql/'
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


