# Dependencies

Bash script used for MySQL/MariaDB/PostgreSQL databases backups over the network with SCP.

# Configuration

Create a `settings.yaml` file for your settings, based on `settings_example.yaml`, and fill in the settings according to the comments. If you don't want to save remotely, leave the `remote.host` empty.

Don't forget to make the local directory where the dumps will be saved (whose path is `local.path` in the settings file) writable by the user www-data or whoever user is running the script.
For PostgreSQL, since it's the system user `postgres.system_user` which will dump the database, I suggest to make the PostgreSQL user owning the directory:
```sh
chown -R postgres:postgres /home/myUser/dumps/
```

Same on the distant server, don't forget to make the backup folder (whose path is `remote.path` in the settings file) writable by the SCP user (the `remote.user` in the settings file).


# Run

Run the script with:
```bash
sudo bash backup_databases.sh
```

# Run with a cron

You can use the scripts with a Linux cron. Edit your root crontab with `crontab -e` and add those lines, for example:

```
# Backup databases every Monday and Thursday at 6:00
0 6 * * 1,4 sh main.py > /root/database-backup-over-scp/log-last-cron.log
```

In this case, don't forget to make your script executable by your cron user, with something like this as your cron user:
```bash
chmod +x main.py
```
