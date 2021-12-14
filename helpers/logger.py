from datetime import datetime

from settings import LOGFILE


class FileLogger:
    def __init__(self) -> None:
        """
        Open log file
        https://stackoverflow.com/questions/2513479/redirect-prints-to-log-file
        """
        self.log_file = open(LOGFILE, "w")

    def log(self, message: str) -> None:
        """
        Output message with readable millisecond time in log file
        """
        print(f"> {message}")
        time: str = datetime.utcnow().strftime("%m/%d %H:%M:%S/%f")[:17]
        self.log_file.write(f"{time}: {message}\n")

    def close(self) -> None:
        """
        Close log file
        """
        self.log_file.close()
