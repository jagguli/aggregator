from datetime import datetime
from src.common.models import get_database, get_collection
from src.scraper.models import Article
from uuid import uuid4

import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from src.scraper.viewsets import ArticleSearchViewset


@pytest.mark.django_db
def test_search_keyword(rf):
    key = "article%s" % datetime.utcnow().strftime("%Y%m%d%H%M%s")
    body = "some news article with isentia %s" % datetime.utcnow()
    article = Article(
        _id=key,
        title="some title",
        body=body,
        published=datetime.utcnow(),
        scraped=datetime.utcnow(),
    )
    article.save()
    key = "article2%s" % datetime.utcnow().strftime("%Y%m%d%H%M%s")
    body = "some news article with %s" % datetime.utcnow()
    article = Article(
        _id=key,
        title="some title",
        body=body,
        published=datetime.utcnow(),
        scraped=datetime.utcnow(),
    )
    article.save()
    request = rf.get(
        "/articles/search/",
        dict(
            q="isentia",
            limit=10,
            offset=0,
        ),
    )

    response = ArticleSearchViewset.as_view({"get": "list"})(request)
    assert response.status_code is 200
    results = response.data
    assert len(results["results"]) == 1
    get_collection(Article.COLLECTION).drop()
