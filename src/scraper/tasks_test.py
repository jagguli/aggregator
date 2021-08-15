import logging
from src.scraper.tasks import crawl, DefaultCrawlSpider as Spider
import requests
import pytest
from scrapy.http import HtmlResponse
import ipdb


@pytest.mark.vcr()
def test_parse_theconversation():
    url = "https://theconversation.com/media-and-politicians-often-defer-to-the-ama-on-covid-policies-but-what-role-should-the-doctors-group-have-in-the-pandemic-165074"
    response = requests.get(url)
    scrapy_response = HtmlResponse(url, body=response.content)

    spider = Spider("theconversation_au")
    results = spider.parse(scrapy_response)
    for result in results:
        print(results)
    ipdb.set_trace()  ######## FIXME:REMOVE ME steven.joseph ################
    assert result == target


def test_crawl(caplog):
    caplog.set_level(logging.ERROR, logger="scrapy")

    deferred = crawl("theconversation_au")

    @deferred.addCallback
    def _success(results):
        """
        After crawler completes, this function will execute.
        Do your assertions in this function.
        """
        import ipdb

        ipdb.set_trace()  ######## FIXME:REMOVE ME steven.joseph ################

    @deferred.addErrback
    def _error(failure):
        raise failure.value

    return deferred
