import pytest
import time
from crawler_rocket.crawler_writer import CrawlerWriter
from crawler_rocket.logger import CH_LOGGER


class Test_crawler_writer:
    def test_init_writer(self):
        writer = CrawlerWriter("key1", ["col1", "col2"])
        assert writer != None
        assert len(writer.columns()) == 2
        assert writer._key == "key1"

    def test_write(self):
        writer = CrawlerWriter("key1", ["col1", "col2"])
        writer.write(0, "col1", 1)
        writer.write(0, 1, 2)
        writer.write(1, "col1", 3)
        writer.write(1, 1, 4)
        writer.write_line(col1=1, col2=2)
        writer.write_line_at(0, col1=10, col2=12)
        assert writer.lines() == 3

    def test_delete(self):
        writer = CrawlerWriter("key1", ["col1", "col2"])
        writer.write(0, "col1", 1)
        writer.write(0, 1, 2)
        writer.write(1, "col1", 3)
        writer.write(1, 1, 4)
        assert writer.lines() == 2
        writer.delete_line(0)
        assert writer.lines() == 1

    def test_append_column(self):
        writer = CrawlerWriter("key1", ["col1", "col2"])
        writer.write_line(col1=1, col2="af")
        writer.write_line(col1=3, col2="df")
        writer.append_column(2, "col3", 0.0, False)
        assert len(writer.columns()) == 3
        writer.delete_column("col1", None)

    def test_apply(self):
        writer = CrawlerWriter("key1", ["col1", "col2"])
        writer.write_line(col1=1, col2="af")
        writer.write_line(col1=3, col2="df")
        writer.apply(0, lambda x: x + 1)
        assert writer.find(0, "col1") == 2

    def test_append(self):
        writer = CrawlerWriter("key1", ["col1", "col2"])
        writer.write_line(col1=1, col2="af")
        writer.write_line(col1=2, col2="df")
        CH_LOGGER.info(writer.data())
        writer1 = CrawlerWriter("key2", ["col1", "col2"])
        writer1.write_line(col1=3, col2="af")
        writer1.write_line(col1=4, col2="df")
        CH_LOGGER.info(writer1.data())
        writer2 = writer.append(writer1)
        CH_LOGGER.info(writer2.data())

    def test_merge(self):
        writer = CrawlerWriter("key1", ["col1", "col2"])
        writer.write_line(col1=1, col2="af")
        writer.write_line(col1=2, col2="df")
        writer1 = CrawlerWriter("key2", ["col1", "col2"])
        writer1.write_line(col1=3, col2="af")
        writer1.write_line(col1=4, col2="df")
        writer2 = writer.merge(writer1, how="left")
        assert writer2.lines() == 2
