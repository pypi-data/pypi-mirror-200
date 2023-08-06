import pytest
from crawler_rocket import logger


class Test_logger:
    def test_debuge_info(self):
        logger.CH_LOGGER.debug("this is debug log")

    def test_log_info(self):
        logger.CH_LOGGER.info("this is info log")

    def test_log_error(self):
        logger.CH_LOGGER.error("this is error log")
