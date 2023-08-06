# MODULES
import sys
import logging


def setup_logger(platform: str):

    if platform is not None:
        platform = platform.lower()

    match platform:
        case "windows":
            logger = logging.getLogger(name="clustering")
            logger.setLevel(logging.INFO)

            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)

            logger.addHandler(handler)
        case _:
            logging.basicConfig(
                filename="clustering.log",
                level=logging.INFO,
            )

            logger = logging.getLogger()

    return logger
