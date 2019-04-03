## PostgreSQL database details to which backup to be done.
POSTGRES_DB_NAMES = ['db1_name','db2_name'] # PostgreSQL databases to backup
POSTGRES_SYSTEM_USER = 'postgres' # make sure this user having enough privileges to take all databases backup.

## MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
MYSQL_DB_NAMES = ['db1_name','db2_name'] # MySQL databases to backup
MYSQL_USER = ''
MYSQL_USER_PASSWORD = ''

## Local setting
LOCAL_PATH = '/root/backup-sql/dumps/' # full local path where dumps will be saved, with trailing slash.
LOGFILE = '/root/backup-sql/log-last-script.log' # full path to log file.

### Remote settings
REMOTE_URL = '' # leave blank if you don't want to save remotely
REMOTE_USER = '' # you need to be authorized on remote with your user SSH keys.
REMOTE_PATH = '/home/backup-sql/' # full remote path where dumps will be saved.
