# Dependencies

Python script used for MySQL/MariaDB/PostgreSQL databases backups, using Python3 (>=3.10), mysqldump utility, pg_dump, Paramiko/SSHClient and Paramiko/SCPClient.

# Configuration

Create a `settings.py` file for your settings, based on `settings_example.py`, and fill in the settings according to the comments. If you don't want to save remotely, leave the `REMOTE_HOST` empty.

The configuration supports individual settings for each database. You can:
- Use default settings for all databases by setting the `*_DEFAULT_*` variables
- Override settings for specific databases in the `*_DATABASES` dictionaries
- Comment out databases you don't want to backup

Example of database-specific configuration:
```python
POSTGRES_DATABASES = {
    "db1_name": {
        "user": POSTGRES_DEFAULT_USER,
        "password": POSTGRES_DEFAULT_PASSWORD,
        "port": POSTGRES_DEFAULT_PORT,
    },
    "db2_name": {
        "user": "custom_user",  # custom user for this database
        "password": "custom_password",
        "port": 5433,  # custom port
    },
}
```

Don't forget to make the local directory where the dumps will be saved (whose path is `LOCAL_PATH` in the settings file) writable by the user www-data or whoever user is running the script.
For PostgreSQL, since it's the system user specified in the database configuration which will dump the database, I suggest to make the PostgreSQL user owning the directory:
```sh
chown -R postgres:postgres /root/dumps/
```

Same on the distant server, don't forget to make the backup folder (whose path is `REMOTE_PATH` in the settings file) writable by the SCP user (the `REMOTE_USER` in the settings file).

# Run

The script is self-executable with [uv](https://docs.astral.sh/uv/). Just make it executable and run it:
```bash
chmod +x main.py
./main.py
```

Or run it directly with uv:
```bash
uv run main.py
```

# Run with a cron

You can use the scripts with a Linux cron. Edit your root crontab with `crontab -e` and add those lines, for example:

```
# Backup databases every Monday and Thursday at 6:00
0 6 * * 1,4 /root/database-backup-over-scp/main.py > /root/database-backup-over-scp/log-last-cron.log
```

# Lint and format the code

To lint, format and sort imports:
```bash
uvx ruff check --fix && uvx ruff format
```
