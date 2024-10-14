import logging
import sys


def setup_logger():
    logger = logging.getLogger("myapp")
    logger.setLevel(logging.INFO)

    # 標準出力へのハンドラを設定
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


logger = setup_logger()
