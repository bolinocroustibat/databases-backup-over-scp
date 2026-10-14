# Logging settings
LOG_LEVEL = "INFO"  # Available levels: DEBUG, INFO, WARNING, ERROR, SUCCESS

# PostgreSQL database details to which backup to be done.
# Used only by backup-postgresql.py script.
POSTGRES_DEFAULT_USER = (
    "postgres"  # make sure this system user has enough privileges to take all databases backup.
)
POSTGRES_DEFAULT_PASSWORD = "postgres"
POSTGRES_DEFAULT_PORT = 5432

# Each entry below is an example pattern (defaults, custom settings, Docker). Replace names
# with your real database names and remove or comment out blocks you do not use.
POSTGRES_DATABASES = {
    # Example: local PostgreSQL with the default user, password, and port.
    "db1_name": {
        "user": POSTGRES_DEFAULT_USER,
        "password": POSTGRES_DEFAULT_PASSWORD,
        "port": POSTGRES_DEFAULT_PORT,
    },
    # Example: local PostgreSQL with a custom user, port, and dump timeout.
    # timeout is optional, in seconds (default 300). Raise it for large dumps.
    "db2_name": {
        "user": "custom_user",
        "password": "custom_password",
        "port": 5433,
        "timeout": 120,
    },
    # Example: Docker PostgreSQL with no port published on the host (see README).
    # pg_dump runs inside the container; port is ignored. Also avoids a host pg_dump
    # that is older than the server (e.g. PostgreSQL 17).
    "db3_name": {
        "user": "custom_user",
        "password": "custom_password",
        "container": "postgres17",
        "timeout": 600,
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
    # Example: local MySQL with the default user, password, and port.
    "db1_name": {
        "user": MYSQL_DEFAULT_USER,
        "password": MYSQL_DEFAULT_PASSWORD,
        "port": MYSQL_DEFAULT_PORT,
    },
    # Example: custom user, port, and dump timeout.
    # timeout is optional, in seconds (default 300). Raise it for large dumps.
    "db2_name": {
        "user": "custom_user",
        "password": "custom_password",
        "port": 3307,
        "timeout": 120,
    },
}

# Local setting
LOCAL_PATH = (
    "sql_dumps/"  # local path where dumps will be saved, relative to the script's directory
)

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
