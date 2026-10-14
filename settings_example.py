# Logging settings
LOG_LEVEL = "INFO"  # Available levels: DEBUG, INFO, WARNING, ERROR, SUCCESS

# System user that runs pg_dump via sudo for local PostgreSQL (not a Docker container).
# This user needs enough privileges to dump every database listed below.
POSTGRES_SYSTEM_USER = "postgres"

# Replace the names with your real database names and remove blocks you do not use.
POSTGRES_DATABASES = {
    # Local server. user is the database role, not the system user above.
    "db1_name": {
        "user": "postgres",
        "password": "postgres",
        "port": 5432,
    },
    # Docker, no host port. pg_dump runs in the container; port is ignored.
    # timeout is optional, in seconds (default 300). Raise it for large dumps.
    "db2_name": {
        "user": "postgres",
        "password": "postgres",
        "container": "postgres17",
        "timeout": 600,
    },
}

# Replace the names with your real database names and remove blocks you do not use.
MYSQL_DATABASES = {
    # Local server, default port.
    "db1_name": {
        "user": "mysql_user",
        "password": "mysql_password",
        "port": 3306,
    },
    # Custom port.
    # timeout is optional, in seconds (default 300). Raise it for large dumps.
    "db2_name": {
        "user": "mysql_user",
        "password": "mysql_password",
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
