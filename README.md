# Database Backup and Monitoring Scripts

# Description

This project consists of Python scripts designed to automate backup processes for MariaDB and MongoDB databases, as well as query scripts for monitoring purposes. The backup scripts ensure data integrity and disaster recovery capabilities, while the monitoring scripts provide insights into the database login and unaunthorised access

# Features

- Automated backup processes for MariaDB and MongoDB databases.
- Query scripts for database login and unaunthorised access.


# Technologies Used

 - Python
 - MariaDB
 - MongoDB
    
# Installation

  - Clone the repository.
  - Install the required Python packages using `pip install -r requirements.txt`.
  - Ensure access to the MariaDB and MongoDB databases is configured correctly.

# Usage

# Backup Scripts

  Configure the backup settings in `backup-config.cnf`.
  Run `mariadb_backup.py` to backup MariaDB databases.
  Run `mongodb_backup.py` to backup MongoDB databases.

# Monitoring Scripts

  Run `Queries-login.py` and `Queries-unauthorized.py` to execute database queries for monitoring purposes.
  Analyze the output for login and unaunthorised access.


# License
This project is licensed under the MIT License.

# Contact

For any questions or feedback, please contact me at devprecious@gmail.com.
