from datetime import datetime

from settings import LOGFILE


class FileLogger:
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    def __init__(self) -> None:
        """
        Open log file
        https://stackoverflow.com/questions/2513479/redirect-prints-to-log-file
        """
        self.log_file = open(LOGFILE, "w")

    def log_write_file(self, message: str) -> None:
        """
        Output message with readable millisecond time in log file
        """
        time: str = datetime.utcnow().strftime("%m/%d %H:%M:%S/%f")[:17]
        self.log_file.write(f"{time}: {message}\n")

    def log(self, message: str) -> None:
        print(f"{self.PURPLE}{message}{self.ENDC}")
        self.log_write_file(message)

    def debug(self, message: str) -> None:
        print(f"{self.CYAN}{message}{self.ENDC}")
        self.log_write_file(message)

    def warning(self, message: str) -> None:
        print(f"{self.YELLOW}{message}{self.ENDC}")
        self.log_write_file(message)

    def error(self, message: str) -> None:
        print(f"{self.RED}{message}{self.ENDC}")
        self.log_write_file(message)

    def success(self, message: str) -> None:
        print(f"{self.GREEN}{message}{self.ENDC}")
        self.log_write_file(message)

    def close(self) -> None:
        """
        Close log file
        """
        self.log_file.close()
