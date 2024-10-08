# PostgreSQL database details to which backup to be done.
# Used only by backup-postgresql.py script.
POSTGRES_DB_NAMES = ["db1_name", "db2_name"]  # PostgreSQL databases names to backup.
POSTGRES_SYSTEM_USER = "postgres"  # make sure this system user has enough privileges to take all databases backup. # noqa E501
POSTGRES_PASSWD = ""
POSTGRES_PORT = 5432  # PostgreSQL port.

# MySQL database details to which backup to be done.
# Used only by backup-mysql.py script.
MYSQL_DB_NAMES = ["db1_name", "db2_name"]  # MySQL databases to backup
MYSQL_USER = ""  # make sure this MySQL user has enough privileges to take all databases backup.
MYSQL_USER_PASSWORD = ""

# Local setting
LOCAL_PATH = "/root/databases-backup-over-scp/dumps/"  # full local path where dumps will be saved, with trailing slash. # noqa E501
LOGFILE = "/root/databases-backup-over-scp/log-last-script.log"  # full path to log file.

# Remote settings
REMOTE_HOST = ""  # leave blank if you don't want to save remotely.
REMOTE_USER = ""  # you need to be authorized on remote with your user SSH keys.
REMOTE_PATH = "/home/backup-sql/"  # full remote path where dumps will be saved.
