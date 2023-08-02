import subprocess
from datetime import datetime
from typing import Optional

from settings import LOCAL_PATH, POSTGRES_SYSTEM_USER


def create_local_folder(logger) -> Optional[str]:
    """
    Create local backup folder
    Returns the path of the created folder if successful, None otherwise
    """
    now: str = datetime.utcnow().strftime("%Y-%m-%d--%H-%M")
    local_path = LOCAL_PATH + now
    if POSTGRES_SYSTEM_USER:
        # If we have a postgre system user, we create the folder as owned by it
        # so it can also be writable by the postgresql script using the same folder
        cmd: str = f'su - {POSTGRES_SYSTEM_USER} -c "mkdir -p {local_path}"'
    else:
        cmd: str = f"mkdir -p {local_path}"
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    proc.wait()
    (stdout, stderr) = proc.communicate()

    if stderr:
        logger.error(f"Error while creating local backup folder: {stderr.decode()}")

    else:
        logger.success(f"Local backup folder {local_path} created.")
        return local_path
