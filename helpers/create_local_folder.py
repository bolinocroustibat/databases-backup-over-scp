import subprocess
from datetime import UTC, datetime
from pathlib import Path

from settings import LOCAL_PATH, POSTGRES_DEFAULT_USER


def create_local_folder(logger) -> Path | None:
    """
    Create local backup folder
    Returns the path of the created folder if successful, None otherwise
    """
    now: str = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M")
    base_path = Path(LOCAL_PATH)
    local_path = base_path / now
    logger.debug(f"Creating local backup folder: {local_path}")

    try:
        # First create the base directory if it doesn't exist
        base_path.mkdir(parents=True, exist_ok=True)

        # Create the timestamped directory
        local_path.mkdir(parents=True, exist_ok=True)

        if POSTGRES_DEFAULT_USER:
            logger.debug(f"Using PostgreSQL user: {POSTGRES_DEFAULT_USER}")
            # If we have a postgre system user, we create the folder as owned by it
            # so it can also be writable by the postgresql script using the same folder
            cmd: str = f"chown -R {POSTGRES_DEFAULT_USER}:{POSTGRES_DEFAULT_USER} {local_path}"
            subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )

        logger.success(f"Local backup folder {local_path} created.")
        return local_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while setting permissions on local backup folder: {e.stderr}")
        return None
    except Exception as e:
        logger.error(f"Error while creating local backup folder: {str(e)}")
        return None
