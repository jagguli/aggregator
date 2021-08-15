from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from src.scraper.tasks import crawl


class Command(BaseCommand):
    help = "Scrape targets"

    def handle(self, *args, **options):
        crawl.delay("theconversation")
        print("triggered crawl")
