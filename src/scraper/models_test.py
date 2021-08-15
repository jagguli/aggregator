from src.scraper.models import Article
from src.common.models import get_database, get_collection
from datetime import datetime


def test_key_put():
    key = "article%s" % datetime.utcnow().strftime("%Y%m%d%H%M%s")
    body = "somebody %s" % datetime.utcnow()
    article = Article(
        _id=key,
        title="some title",
        body=body,
        published=datetime.utcnow(),
        scraped=datetime.utcnow(),
    )
    article.save()
    result = get_database()[Article.COLLECTION].find_one({"_id": key})
    assert result is not None
    assert result["_id"] == key
    get_collection(Article.COLLECTION).drop()


def test_body_search():
    key = "article search 1%s" % datetime.utcnow().strftime("%Y%m%d%H%M%s")
    body = "somebody %s" % datetime.utcnow()
    article = Article(
        _id=key,
        title="some title",
        body=body,
        published=datetime.utcnow(),
        scraped=datetime.utcnow(),
    )
    article.save()
    key = "article search 2%s" % datetime.utcnow().strftime("%Y%m%d%H%M%s")
    body = "somebody else %s" % datetime.utcnow()
    article = Article(
        _id=key,
        title="some title",
        body=body,
        published=datetime.utcnow(),
        scraped=datetime.utcnow(),
    )
    article.save()
    results = [x for x in Article.search("somebody")]
    assert len(results) == 2
    get_collection(Article.COLLECTION).drop()
