from rest_framework.routers import SimpleRouter
from src.scraper.viewsets import ArticleSearchViewset

scraper_router = SimpleRouter()

scraper_router.register(
    r"articles/search",
    ArticleSearchViewset,
    basename="articles-search",
)
