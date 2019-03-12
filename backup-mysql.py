#!/usr/bin/python
###########################################################
# This python script is used for MySQL databases backup
# using mysqldump utility, Paramiko/SSHClient and Paramiko/SCPClient
# Last modified: Jan 31, 2019 by bolino (https://adriencarpentier.com)
##########################################################


#########################################
#               SETTINGS                #
#########################################

#### MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup. 
DB_USER = ''
DB_USER_PASSWORD = ''
DB_NAMES = ['db1_name','db2_name'] # list of databases names (strings separated by commas)

### Local setting
LOCAL_PATH = '/root/backup-sql/dump/' # full local path where dumps will be saved, with trailing slash
LOGFILE = '/root/backup-sql/log-last-script.log' # full path to log file

#######################################
#               SCRIPT                #
#######################################

### Import required Python libraries
import os, sys, time
from datetime import datetime

### Open log file and redirects print to log file (https://stackoverflow.com/questions/2513479/redirect-prints-to-log-file)
old_stdout = sys.stdout
log_file = open(LOGFILE,"w")
sys.stdout = log_file

### Function to have readable millisecond time in log file
def logtime():
	return(datetime.utcnow().strftime('%d/%m %H:%M:%S/%f')[:17])

### Getting current datetime and get full path names including datetime "2017-01-26--07-13-34".
DATETIME = time.strftime('%Y-%m-%d--%H-%M-%S')
TODAY_LOCAL_PATH = LOCAL_PATH + DATETIME

### Create local backup folder
try:
	os.makedirs(TODAY_LOCAL_PATH)
	print(logtime() + ": Local backup folder " + TODAY_LOCAL_PATH + " created.\n")
except:
	print(logtime() + ": ### ERROR ### while creating local backup folder!\n")

### Starting actual databases backup process
for db in DB_NAMES:
	try:
		### Backup locally
		dumpcmd = "mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + TODAY_LOCAL_PATH + "/" + db + ".sql"
		os.system(dumpcmd)
		print(logtime() + ": Backup file " + db + ".sql has been saved locally.\n")
	except Exception as e:
			print(logtime() + ": Error while trying to dump the database locally.\n")
			print(e + "\n")

print(logtime() + ": Backup script completed.\n")

### Close log file
sys.stdout = old_stdout
log_file.close()
