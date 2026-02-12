import subprocess
from datetime import UTC, datetime
from pathlib import Path

from settings import LOCAL_PATH, POSTGRES_DEFAULT_USER


def create_local_folder(logger) -> Path | None:
    """
    Create local backup folder.

    If POSTGRES_DEFAULT_USER is set, the folder is given group postgres and mode 2775
    (setgid + rwxrwxr-x) so that:
    - The current user stays owner and can create new timestamped dirs on the next run.
    - The postgres user can write dumps (group write). The script user must be in group
      postgres for chgrp to succeed (e.g. usermod -aG postgres $USER, then re-login).

    Returns the path of the created folder if successful, None otherwise.
    """
    now: str = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M")
    base_path = Path(LOCAL_PATH).resolve()
    local_path = base_path / now
    logger.debug(f"Creating local backup folder: {local_path}")

    try:
        # First create the base directory if it doesn't exist
        base_path.mkdir(parents=True, exist_ok=True)

        # Create the timestamped directory
        local_path.mkdir(parents=True, exist_ok=True)

        if POSTGRES_DEFAULT_USER:
            logger.debug(f"Using PostgreSQL user (group + setgid): {POSTGRES_DEFAULT_USER}")
            # Keep ownership with current user; give group to postgres and 2775 so
            # postgres can write dumps and we can still create new dirs on next run.
            for path in (base_path, local_path):
                subprocess.run(
                    ["chgrp", POSTGRES_DEFAULT_USER, str(path)],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                subprocess.run(
                    ["chmod", "2775", str(path)],
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
