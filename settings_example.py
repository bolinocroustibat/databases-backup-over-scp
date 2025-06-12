# Logging settings
LOG_LEVEL = "INFO"  # Available levels: DEBUG, INFO, WARNING, ERROR, SUCCESS
LOGFILE = "log-last-script.log"  # log file will be created in the script's directory (relative path)

# PostgreSQL database details to which backup to be done.
# Used only by backup-postgresql.py script.
POSTGRES_DEFAULT_PORT = 5432
POSTGRES_DEFAULT_USER = (
    "postgres"  # make sure this system user has enough privileges to take all databases backup.
)
POSTGRES_DEFAULT_PASSWORD = "postgres"

POSTGRES_DATABASES = {
    "db1_name": {
        "user": POSTGRES_DEFAULT_USER,
        "password": POSTGRES_DEFAULT_PASSWORD,
        "port": POSTGRES_DEFAULT_PORT,
    },
    "db2_name": {
        "user": "custom_user",  # example of custom user for specific database
        "password": "custom_password",
        "port": 5433,  # example of custom port
    },
}

# MySQL database details to which backup to be done.
# Used only by backup-mysql.py script.
MYSQL_DEFAULT_USER = (
    ""  # make sure this MySQL user has enough privileges to take all databases backup.
)
MYSQL_DEFAULT_PASSWORD = ""
MYSQL_DEFAULT_PORT = 3306

MYSQL_DATABASES = {
    "db1_name": {
        "user": MYSQL_DEFAULT_USER,
        "password": MYSQL_DEFAULT_PASSWORD,
        "port": MYSQL_DEFAULT_PORT,
    },
    "db2_name": {
        "user": "custom_user",  # example of custom user for specific database
        "password": "custom_password",
        "port": 3307,  # example of custom port
    },
}

# Local setting
LOCAL_PATH = "dumps/"  # local path where dumps will be saved, relative to the script's directory

# Remote settings
REMOTE_HOST = ""  # leave blank if you don't want to save remotely.
REMOTE_USER = ""  # you need to be authorized on remote with your user SSH keys.
REMOTE_PATH = "/home/backup-sql/"  # full remote path where dumps will be saved.
