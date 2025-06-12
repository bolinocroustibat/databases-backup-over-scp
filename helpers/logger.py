from datetime import UTC, datetime

from settings import LOG_LEVEL, LOGFILE


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

    # Define log levels and their hierarchy
    LEVELS = {
        "DEBUG": 0,
        "INFO": 1,
        "WARNING": 2,
        "ERROR": 3,
        "SUCCESS": 4,
    }

    def __init__(self) -> None:
        """
        Open log file
        https://stackoverflow.com/questions/2513479/redirect-prints-to-log-file
        """
        self.log_file = open(LOGFILE, "w")
        self.min_level = self.LEVELS.get(LOG_LEVEL, self.LEVELS["INFO"])

    def _should_log(self, level: str) -> bool:
        """Check if the message should be logged based on LOG_LEVEL"""
        return self.LEVELS.get(level, 0) >= self.min_level

    def log_write_file(self, message: str) -> None:
        """
        Output message with readable millisecond time in log file
        """
        time: str = datetime.now(UTC).strftime("%m/%d %H:%M:%S/%f")[:17]
        self.log_file.write(f"{time}: {message}\n")

    def log(self, message: str) -> None:
        if self._should_log("INFO"):
            print(f"{self.PURPLE}ℹ️ {message}{self.ENDC}")
            self.log_write_file(message)

    def debug(self, message: str) -> None:
        if self._should_log("DEBUG"):
            print(f"{self.CYAN}🔍 {message}{self.ENDC}")
            self.log_write_file(message)

    def warning(self, message: str) -> None:
        if self._should_log("WARNING"):
            print(f"{self.YELLOW}⚠️ {message}{self.ENDC}")
            self.log_write_file(message)

    def error(self, message: str) -> None:
        if self._should_log("ERROR"):
            print(f"{self.RED}❌ {message}{self.ENDC}")
            self.log_write_file(message)

    def success(self, message: str) -> None:
        if self._should_log("SUCCESS"):
            print(f"{self.GREEN}✅ {message}{self.ENDC}")
            self.log_write_file(message)

    def close(self) -> None:
        """
        Close log file
        """
        self.log_file.close()
