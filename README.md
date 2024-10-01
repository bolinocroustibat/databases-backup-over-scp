# Dependencies

Python script used for MySQL/MariaDB/PostgreSQL databases backups, using Python3 (>=3.10), mysqldump utility, pg_dump, Paramiko/SSHClient and Paramiko/SCPClient.

# Configuration

Create a `settings.py` file for your settings, based on `settings_example.py`, and fill in the settings according to the comments. If you don't want to save remotely, leave the `REMOTE_HOST` empty.

Don't forget to make the local directory where the dumps will be saved (whose path is `LOCAL_PATH` in the settings file) writable by the user www-data or whoever user is running the script.
For PostgreSQL, since it's the system user `POSTGRES_SYSTEM_USER` which will dump the database, I suggest to make the PostgreSQL user owning the directory:
```sh
chown -R postgres:postgres /root/dumps/
```

Same on the distant server, don't forget to make the backup folder (whose path is `REMOTE_PATH` in the settings file) writable by the SCP user (the `REMOTE_USER` in the settings file).


# Run

Create a virtual environment with `python3 -m venv .venv`, install packages in it with `pip install .`, and run the script with:
```bash
python3 main.py
```

Or just use [uv](https://docs.astral.sh/uv/):
```bash
uv sync
uv run main.py
```


# Run with a cron

You can use the scripts with a Linux cron. Edit your root crontab with `crontab -e` and add those lines, for example:

```
# Backup databases every Monday and Thursday at 6:00
0 6 * * 1,4 python3 /root/database-backup-over-scp/main.py > /root/database-backup-over-scp/log-last-cron.log
```

In this case, don't forget to make your script executable by your cron user, with something like this as your cron user:
```bash
chmod +x main.py
```

# Lint and frmat the code

To lint, format and sort imports:
```bash
uvx ruff check --fix && uvx ruff format
```
