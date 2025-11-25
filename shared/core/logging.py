import logging
import sys
from typing import Optional


def setup_logging(
    service_name: str,
    level: int = logging.INFO,
    format_string: Optional[str] = None,
) -> None:
    if format_string is None:
        format_string = "%(asctime)s [%(service)s] [%(levelname)s] %(message)s"

    # Create a custom formatter that includes service name
    class ServiceFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            record.service = service_name
            return super().format(record)

    formatter = ServiceFormatter(format_string)

    # Configure root logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

