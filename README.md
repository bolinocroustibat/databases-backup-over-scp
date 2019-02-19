This Python scripts are to be used for MySQL/PostgreSQL databases backups, using mysqldump utility, pg_dump, Paramiko/SSHClient and Paramiko/SCPClient.

Use it with a cron. Edit your root crontab with "crontab -e" and add those lines, for example:

```
# Backup MySQL databases every Tuesday and Friday at 3:00
0 3 * * 2,5 python3 /root/backup-sql/backup-mysql.py > /root/backup-sql/log-last-cron.log
```

```
# Backup PostgreSQL databases every Monday and Thursday at 6:00
0 6 * * 1,4 python3 /root/backup-sql/backup-postgresql.py > /root/backup-sql/log-last-cron.log
```

Don't forget to make your script executable with something like:

```sh
chmod +x backup-sql.py
```

Also, don't forget to make the local backup folder writable by user www-data or whoever user is running the script.
Same on the distant server, don't forget to make the backup folder writable by the SCP user (defined in REMOTE_USER contant in the script).

For PotsgreSQL, since it's the system DB_USER which will dumb the database, I would suggest to make him owning the backup folder:

```sh
chown -R postgres:postgres backup-sql
```
