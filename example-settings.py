## PostgreSQL database details to which backup to be done.
POSTGRES_DB_NAMES = ['db1_name','db2_name'] # PostgreSQL databases to backup
SYSTEM_POSTGRES_USER = 'postgres' # make sure this user having enough privileges to take all databases backup.

## MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
MYSQL_DB_NAMES = ['db1_name','db2_name'] # MySQL databases to backup
MYSQL_USER = ''
MYSQL_USER_PASSWORD = ''

## Local setting
LOCAL_PATH = '/root/backup-sql/' # full local path where dumps will be saved, with trailing slash.
LOGFILE = '/root/backup-sql/log-last-script.log' # full path to log file.
