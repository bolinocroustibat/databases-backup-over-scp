Those two Python scripts are to be used for MySQL/PostgreSQL databases backups, using Python3, mysqldump utility, pg_dump, Paramiko/SSHClient and Paramiko/SCPClient.

# Configuration

Create a `settings.py` file for your settings, based on `settings_example.py`, and fill in the settings according to the comments. If you don't want to save remotely, leave the `REMOTE_HOST` empty.

Don't forget to make the local directory where the dumps will be saved (whose path is `LOCAL_PATH` in the settings file) writable by the user www-data or whoever user is running the script.
For PostgreSQL, since it's the system user `POSTGRES_SYSTEM_USER` which will dump the database, I suggest to make the PostgreSQL user owning the directory:
```sh
chown -R postgres:postgres /root/dumps/
```

Same on the distant server, don't forget to make the backup folder (whose path is `REMOTE_PATH` in the settings file) writable by the SCP user (the `REMOTE_USER` in the settings file).


# Run

Create a virtual environement, activate it, install `paramiko` and `scp` Python packages inside it, and run:

MySQL:
```sh
python3 backup-mysql.py
```

PostgreSQL:
```sh
python3 backup-postgresql.py
```

Or use [Poetry](https://python-poetry.org/) or [PDM](https://pdm.fming.dev/) to run it, with:

MySQL:
```sh
poetry run backup-mysql.py
```
```sh
pdm run backup-mysql.py
```


# Run with a cron

You can use the scripts with a Linux cron. Edit your root crontab with `crontab -e` and add those lines, for example:

```
# Backup MySQL databases every Tuesday and Friday at 3:00
0 3 * * 2,5 python3 /root/database-backup-over-scp/backup-mysql.py > /root/database-backup-over-scp/log-last-cron.log
```
or/and:
```
# Backup PostgreSQL databases every Monday and Thursday at 6:00
0 6 * * 1,4 python3 /root/database-backup-over-scp/backup-postgresql.py > /root/database-backup-over-scp/log-last-cron.log
```

In this case, don't forget to make your script executable by your cron user, with something like this as your cron user:

```sh
chmod +x backup-mysql.py
```
or/and:
```sh
chmod +x backup-postgresql.py
```
