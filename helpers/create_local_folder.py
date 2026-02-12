from datetime import UTC, datetime
from pathlib import Path

from settings import LOCAL_PATH


def create_local_folder(logger) -> Path | None:
    """
    Create local backup folder.

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

        logger.success(f"Local backup folder {local_path} created.")
        return local_path
    except Exception as e:
        logger.error(f"Error while creating local backup folder: {str(e)}")
        return None
