import logging

from celery import shared_task
from celery import signals, Task
from html2text import HTML2Text
from readability import Document
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.signals import item_scraped as item_scraped_signal
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings

from src.config import celery_app as app
from django.core.cache import cache
from src.scraper.models import Article
import hashlib


## https://www.zyte.com/blog/how-to-crawl-the-web-politely-with-scrapy/


def on_item_scraped(item):
    logging.debug("ITEM SCRAPED %(title)s %(url)s" % item)
    article = Article(**item)
    article.save()


class NoContent(Exception):
    pass


def make_readable(text):
    h = HTML2Text()
    h.ignore_links = True
    return h.handle(Document(text).summary()).strip()


class SingletonTask(Task):
    def __call__(self, *args, **kwargs):
        lock = cache.lock(self.name)

        if not lock.acquire(blocking=False):
            logging.info("{} failed to lock".format(self.name))
            return

        try:
            super(SingletonTask, self).__call__(*args, **kwargs)
        except Exception as e:
            lock.release()
            raise e
        lock.release()


class DefaultCrawlSpider(CrawlSpider):
    name = "theconversation"
    allowed_domains = ["theconversation.com"]
    start_urls = ["https://theconversation.com/au"]
    rules = (Rule(LinkExtractor(), callback="parse_article", follow=True),)

    # def parse_start_url(self, response, **kwargs):
    #    return self.start_urls

    def get_authors(self, article):
        return article.css("span.author-name").get()

    def get_tags(self, article):
        return []

    def get_article(self, article):
        article = "\n".join(article.css("div.content-body").getall()).strip()
        if not article:
            raise NoContent("Content not found")
        return make_readable(article)

    def get_title(self, article):
        title = "\n".join(article.css("h1.entry-title").getall()).strip()
        if not title:
            return "Untitled"
        return make_readable(title)

    def parse_article(self, response):
        for article in response.css("article"):
            try:
                yield {
                    "body": self.get_article(article),
                    "title": self.get_title(article),
                    "authors": self.get_authors(article),
                    "tags": self.get_tags(article),
                    "url": response.url,
                    "_id": hashlib.md5(response.url.encode()).hexdigest(),
                }
            except NoContent:
                pass


@shared_task(base=SingletonTask)
def crawl(*args, **kwargs):
    settings = get_project_settings()
    crawler = Crawler(DefaultCrawlSpider, settings)
    crawler.signals.connect(on_item_scraped, signal=item_scraped_signal)
    runner = CrawlerRunner()
    return runner.crawl(crawler)


@signals.worker_process_init.connect
def configure_infrastructure(**kwargs):
    from crochet import setup

    setup()
    print("started new thread")
