import logging
from src.scraper.tasks import crawl, DefaultCrawlSpider as Spider
import requests
import pytest
from scrapy.http import HtmlResponse


@pytest.mark.vcr()
def test_parse_theconversation():
    url = "https://theconversation.com/media-and-politicians-often-defer-to-the-ama-on-covid-policies-but-what-role-should-the-doctors-group-have-in-the-pandemic-165074"
    response = requests.get(url)
    scrapy_response = HtmlResponse(url, body=response.content)

    spider = Spider("theconversation_au")
    results = spider.parse_article(scrapy_response)
    assert len([x for x in results]) > 0


def test_crawl(caplog):
    caplog.set_level(logging.ERROR, logger="scrapy")

    deferred = crawl("theconversation_au")

    @deferred.addCallback
    def _success(results):
        """
        After crawler completes, this function will execute.
        Do your assertions in this function.
        """

    @deferred.addErrback
    def _error(failure):
        raise failure.value

    return deferred
