#!/usr/bin/python
###########################################################
# This python script is used for MySQL databases backup
# using mysqldump utility, Paramiko/SSHClient and Paramiko/SCPClient
# Last modified: Jan 17, 2018 by bolino (http://adriencarpentier.com)
##########################################################


#########################################
#               SETTINGS                #
#########################################

#### MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup. 
DB_HOST = 'localhost'
DB_USER = ''
DB_USER_PASSWORD = ''
DB_NAMES = [] # list of databases names (strings separated by commas)

### Local setting
LOCAL_PATH = '/home/backup-sql/dump/' # full local path where dumps will be saved
LOGFILE = '/home/backup-sql/log-last.log' # full path to log file

### Remote settings
REMOTE_URL = ''
REMOTE_USER = '' # you need to be authorized on remote with your user SSH keys
REMOTE_PATH = '/home/backup-sql/' # full remote path where dumps will be saved


#######################################
#               SCRIPT                #
#######################################

### Import required Python libraries
import os, sys, time
from datetime import datetime
from paramiko import SSHClient  # don't forget to "pip install paramiko" on OS
from scp import SCPClient # don't forget to "pip install scp" on OS

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
TODAY_REMOTE_PATH = REMOTE_PATH + DATETIME

### Connecting to backup server
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(REMOTE_URL, username=REMOTE_USER)
scp = SCPClient(ssh.get_transport()) # SCPCLient takes a paramiko transport as its only argument

### Create local backup folder
try:
	os.makedirs(TODAY_LOCAL_PATH)
	print(logtime() + ": Local backup folder " + TODAY_LOCAL_PATH + " created.\n")
except:
	print(logtime() + ": ### ERROR ### while creating local backup folder!\n")

### Create remote backup folder
try :
	ssh.exec_command('mkdir -p ' + TODAY_REMOTE_PATH)
	ssh.close
	print(logtime() + ": Remote backup folder " + TODAY_REMOTE_PATH + " created on " + REMOTE_URL + "\n")
except :
	print(logtime() + ": ### ERROR ### while creating remote backup folder" + TODAY_REMOTE_PATH + " on " + REMOTE_URL + "\n")

### Starting actual databases backup process
scp = SCPClient(ssh.get_transport()) # Initiates distant file transfer (SCPClient takes a paramiko transport as its only argument)
try:
	for db in DB_NAMES:
		print(logtime() + ": Reading " + db + "...\n")
		dumpcmd = "mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + TODAY_LOCAL_PATH + "/" + db + ".sql"
		os.system(dumpcmd)
		print(logtime() + ": Backup file " + db + ".sql has been saved locally.\n")
		### Copy on remote
		try:
			scp.put(TODAY_LOCAL_PATH + "/" + db + ".sql", TODAY_REMOTE_PATH + "/" + db + ".sql")
			print(logtime() + ": Backup file " + db + ".sql has been copied on remote " + REMOTE_URL + ".\n")
		except:
			print(logtime() + ": ### ERROR ### while tring to copy " + db + ".sql on the remote!\n")	
except:
	print(logtime() + ": ### ERROR ### while backup!\n")
scp.close()

print(logtime() + ": Backup script completed.\n")

### Close log file
sys.stdout = old_stdout
log_file.close()
