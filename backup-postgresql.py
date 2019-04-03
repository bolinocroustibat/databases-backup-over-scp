#!/usr/bin/python

## Import required Python libraries
import os, sys, time
from datetime import datetime
from paramiko import SSHClient  # don't forget to "pip install paramiko" on OS
from scp import SCPClient # don't forget to "pip install scp" on OS

## Import settings
from settings import POSTGRES_DB_NAMES, POSTGRES_SYSTEM_USER, LOGFILE, LOCAL_PATH, REMOTE_PATH, REMOTE_URL, REMOTE_USER

## Open log file and redirects print to log file (https://stackoverflow.com/questions/2513479/redirect-prints-to-log-file)
old_stdout = sys.stdout
log_file = open(LOGFILE,"w")
sys.stdout = log_file

## Function to have readable millisecond time in log file
def logtime():
	return(datetime.utcnow().strftime('%d/%m %H:%M:%S/%f')[:17])

## Getting current datetime for building full path names including datetime "2017-01-26--07-13-34".
DATETIME = time.strftime('%Y-%m-%d--%H-%M-%S')

## Create local backup folder
TODAY_LOCAL_PATH = LOCAL_PATH + DATETIME
try:
	os.system('su -c "mkdir -p ' + TODAY_LOCAL_PATH + '" ' + POSTGRES_SYSTEM_USER)
	print(logtime() + ": Local backup folder " + TODAY_LOCAL_PATH + " created.\n")
except:
	print(logtime() + ": ### ERROR ### while creating local backup folder!\n")

### Create remote backup folder
if REMOTE_PATH and REMOTE_PATH != '':
	TODAY_REMOTE_PATH = REMOTE_PATH + DATETIME
	## Connecting to backup server
	ssh = SSHClient()
	ssh.load_system_host_keys()
	ssh.connect(REMOTE_URL, username=REMOTE_USER)
	try:
		ssh.exec_command('mkdir -p ' + TODAY_REMOTE_PATH)
		ssh.close
		print(logtime() + ": Remote backup folder " + TODAY_REMOTE_PATH + " created on " + REMOTE_URL + "\n")
	except:
		print(logtime() + ": ### ERROR ### while creating remote backup folder" + TODAY_REMOTE_PATH + " on " + REMOTE_URL + "\n")

## Starting actual databases backup process
scp = SCPClient(ssh.get_transport()) # Initiates distant file transfer (SCPClient takes a paramiko transport as its only argument)
for db in POSTGRES_DB_NAMES:
	try:
		## Backup locally
		dumpcmd = 'su -c "pg_dump ' + db + ' > ' + TODAY_LOCAL_PATH + '/' + db + '.sql" ' + POSTGRES_SYSTEM_USER
		os.system(dumpcmd)
		print(logtime() + ": Backup dump file " + db + ".sql has been saved locally.\n")
		## Copy on remote
		if REMOTE_PATH and REMOTE_PATH != '':
			try:
				scp.put(TODAY_LOCAL_PATH + "/" + db + ".sql", TODAY_REMOTE_PATH + "/" + db + ".sql")
				print(logtime() + ": Backup file " + db + ".sql has been copied on remote " + REMOTE_URL + ".\n")
			except Exception as e:
				print(logtime() + ": ### ERROR ### while tring to copy " + db + ".sql on the remote!\n")
				print(e + "\n")
	except Exception as e:
			print(logtime() + ": ### ERROR ### while trying to dump the database locally.\n")
			print(e + "\n")
scp.close()

print(logtime() + ": Backup script completed.\n")

## Close log file
sys.stdout = old_stdout
log_file.close()
