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