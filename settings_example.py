# Logging settings
LOG_LEVEL = "INFO"  # Available levels: DEBUG, INFO, WARNING, ERROR, SUCCESS

# PostgreSQL database details to which backup to be done.
# Used only by backup-postgresql.py script.
POSTGRES_DEFAULT_USER = (
    "postgres"  # make sure this system user has enough privileges to take all databases backup.
)
POSTGRES_DEFAULT_PASSWORD = "postgres"
POSTGRES_DEFAULT_PORT = 5432

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
LOCAL_PATH = "sql_dumps/"  # local path where dumps will be saved, relative to the script's directory

# Remote settings
REMOTE_HOST = ""  # leave blank if you don't want to save remotely.
REMOTE_USER = ""  # you need to be authorized on remote with your user SSH keys.
REMOTE_PATH = "/home/backup_sql/"  # full remote path where dumps will be saved.

# GFS retention (Grandfather-Father-Son). Applied after each backup if RETENTION_ENABLED is True.
# Son (daily): one backup per day, keep the last N days.
# Father (weekly): backup on RETENTION_WEEKLY_DAY (e.g. Sunday), keep the last N weeks. Use 0 to disable.
# Grandfather (monthly): backup on the 1st of the month, keep the last N months.
# Great-grandfather (yearly): backup on 1st January, keep the last N years. Use 0 to disable.
#
# Example: 7 days, no weekly, 12 months, 4 years:
#   RETENTION_DAILY_DAYS = 7
#   RETENTION_WEEKLY_WEEKS = 0
#   RETENTION_MONTHLY_MONTHS = 12
#   RETENTION_YEARLY_YEARS = 4
RETENTION_ENABLED = True
RETENTION_DAILY_DAYS = 7
RETENTION_WEEKLY_WEEKS = 4
RETENTION_WEEKLY_DAY = 6  # 0=Monday, 6=Sunday
RETENTION_MONTHLY_MONTHS = 12
RETENTION_YEARLY_YEARS = 0  # set to 4 to keep the last 4 years (1st Jan each year)
