from datetime import datetime

from settings import LOCAL_PATH, REMOTE_PATH


today: str = datetime.utcnow().strftime("%Y-%m-%d--%H-%M")
TODAY_LOCAL_PATH = LOCAL_PATH + today
TODAY_REMOTE_PATH = REMOTE_PATH + today
