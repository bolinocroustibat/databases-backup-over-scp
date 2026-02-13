# 📦 Dependencies

Python script used for MySQL/MariaDB/PostgreSQL databases backups, using Python3 (>=3.10), mysqldump utility, pg_dump, Paramiko/SSHClient and Paramiko/SCPClient.

# ⚙️ Configuration

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

Don't forget to make the local directory where the dumps will be saved (whose path is `LOCAL_PATH` in the settings file) writable by the user running the script.

**PostgreSQL:** the script runs as your user but executes `pg_dump` as the system user `postgres` (via `sudo -u postgres`). The dump output is piped through stdout so the resulting file is owned by your user — no special group membership is required. The user running the script only needs to be in the sudoers for the `sudo -u postgres` command.

Same on the distant server, don't forget to make the backup folder (whose path is `REMOTE_PATH` in the settings file) writable by the SCP user (the `REMOTE_USER` in the settings file).

# 📅 Retention (GFS)

The script can apply a **Grandfather-Father-Son** retention policy after each backup (enable with `RETENTION_ENABLED = True` in `settings.py`):

- **Son (daily)**: one backup per day is kept for the last N days (default: 7).
- **Father (weekly)**: the backup of the chosen weekday (e.g. Sunday) is kept for the last N weeks (default: 4). Set to 0 to disable.
- **Grandfather (monthly)**: the backup of the 1st of each month is kept for the last N months (default: 12).
- **Great-grandfather (yearly)**: the backup of 1st January is kept for the last N years. Set to 4 for “7 days, no weekly, 12 months, 4 years”. Set to 0 to disable (default).

Only backup folders whose names match `YYYY-MM-DD_HH-MM` are considered. Retention is applied locally and on the remote host when configured.

# ▶️ Run

The script is self-executable with [uv](https://docs.astral.sh/uv/). Just make it executable and run it:
```bash
chmod +x main.py
./main.py
```

Or run it directly with uv:
```bash
uv run main.py
```

# ⏰ Run with a cron

With the GFS retention policy, **run the script once per day**. The retention logic uses the backup folder date (from its name `YYYY-MM-DD_HH-MM`), so:

- Every run creates a daily backup; the last 7 days are kept (Son).
- The run that falls on Sunday is also kept as weekly (Father), if `RETENTION_WEEKLY_WEEKS > 0`.
- The run that falls on the 1st of the month is also kept as monthly (Grandfather).
- The run that falls on 1 January is also kept as yearly (Great-grandfather), if `RETENTION_YEARLY_YEARS > 0`.

One cron entry is enough; no need for separate “daily”, “weekly” or “monthly” jobs.

Example: run every day at 2:00 AM (server timezone). Adjust the path to your install directory:

```bash
# Edit crontab (e.g. for the user that owns the backup dir and has DB access)
crontab -e
```

Add a line like:

```
# Daily backup at 2:00 AM; stdout and stderr go to the log file
0 2 * * * cd /path/to/databases-backup-over-scp && uv run main.py >> cron.log 2>&1
```

Or with the script’s own log file only (the script logs to dated files in `logs/` (e.g. `logs/2025-02-12.log`):

```
0 2 * * * cd /path/to/databases-backup-over-scp && uv run main.py
```

Use an absolute path for `cd` so the script always runs in the right directory (and `LOCAL_PATH` in settings is relative to that).

# 🤝 Contributing

Before contributing to the repository and making any PR, it is necessary to initialize the pre-commit hooks:
```bash
pre-commit install
```
Once this is done, code formatting and linting, as well as import sorting, will be automatically checked before each commit.

If you cannot use pre-commit, it is necessary to format, lint, and sort imports with [Ruff](https://docs.astral.sh/ruff/) before committing:
```bash
uv run ruff check --fix . && uv run ruff format .
```
