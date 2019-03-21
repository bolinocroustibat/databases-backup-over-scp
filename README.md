This two Python scripts are to be used for MySQL/PostgreSQL databases backups, using Python3, mysqldump utility, pg_dump, Paramiko/SSHClient and Paramiko/SCPClient.

# Configuration

Create a settings.py file for your settings, based on example_settings.py, and fill in the settings according to the comments. If you don't want to save remotely, leave the REMOTE_URL empty.

Don't forget to make the local directory where the dumps will be saved (whose path is LOCAL_PATH in the settings file) writable by the user www-data or whoever user is running the script.
For PostgreSQL, since it's the system user POSTGRES_SYSTEM_USER which will dump the database, I would suggest to make him owning the directory:

```sh
chown -R postgres:postgres /root/backup-sql/dumps/
```

Same on the distant server, don't forget to make the backup folder (whose path is REMOTE_PATH in the settings file) writable by the SCP user (the REMOTE_USER in the settings file).


# Run with a cron

You can use the scripts with a cron. Edit your root crontab with "crontab -e" and add those lines, for example:

```
# Backup MySQL databases every Tuesday and Friday at 3:00
0 3 * * 2,5 python3 /root/backup-sql/backup-mysql.py > /root/backup-sql/log-last-cron.log
```

```
# Backup PostgreSQL databases every Monday and Thursday at 6:00
0 6 * * 1,4 python3 /root/backup-sql/backup-postgresql.py > /root/backup-sql/log-last-cron.log
```

In this case, don't forget to make your script executable with something like:

```sh
chmod +x backup-mysql.py
```
