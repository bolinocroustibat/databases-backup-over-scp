# 📦 Dependencies

Python script used for MySQL/MariaDB/PostgreSQL databases backups, using Python3 (>=3.11), mysqldump utility, pg_dump, Paramiko/SSHClient and Paramiko/SCPClient.

# ⚙️ Configuration

Create a `settings.py` file for your settings, based on `settings_example.py`, and fill in the settings according to the comments. If you don't want to save remotely, leave the `REMOTE_HOST` empty.

Each database has its own user, password, and port in `POSTGRES_DATABASES` or `MYSQL_DATABASES`.

`POSTGRES_SYSTEM_USER` is the system account used for `sudo -u` when dumping a local PostgreSQL server. It is separate from the database role in each entry.

Example configuration (placeholder names; keep only the entries you need, and comment out or delete the rest):
```python
POSTGRES_SYSTEM_USER = "postgres"

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
```

Don't forget to make the local directory where the dumps will be saved (whose path is `LOCAL_PATH` in the settings file) writable by the user running the script.

**PostgreSQL:** the script runs as your user but executes `pg_dump` as `POSTGRES_SYSTEM_USER` (via `sudo -u`). The dump output is piped through stdout so the resulting file is owned by your user — no special group membership is required. The user running the script only needs to be in the sudoers for that `sudo -u` command. The `user` on each database is the PostgreSQL role passed to `pg_dump -U`.

**PostgreSQL in Docker:** use this when PostgreSQL runs in a container **without a port published on the host** (only reachable on Docker's internal network). Set `container` to the container name: the script runs that container's `pg_dump` with `sudo docker exec` and no `-t`, so the client talks to the server inside the container (local socket / loopback). A dump via `127.0.0.1` on the host would fail in that setup because nothing listens on the host. The container client also matches the server major version (for example PostgreSQL 17); the host `pg_dump` may be too old. Custom format (`-Fc`) is binary, and a TTY would corrupt it. The shell redirect stays on the host, so the dump file is written locally and owned by your user. `port` is ignored when `container` is set. Leave `container` unset or empty when PostgreSQL is exposed on the host (for example `ports: "5432:5432"`) and use the default local dump to `127.0.0.1` and `port`. The user running the script needs passwordless sudo for `docker`.

Optional `timeout` (seconds, default `300`) sets the dump timeout for that MySQL or PostgreSQL database. Raise it for large dumps.

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

# 🚀 Releasing

Push a version tag to create a GitHub Release (version from the tag; release notes are generated automatically). See the repo’s **Releases** page after pushing.

```bash
git tag v0.7.0
git push origin v0.7.0
```

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
