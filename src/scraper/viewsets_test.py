from datetime import datetime
from uuid import uuid4

import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from src.scraper.viewsets import ArticleSearchViewset


@pytest.mark.django_db
def test_search_keyword(rf):
    request = rf.get(
        "/articles/search/",
        dict(
            search="isentia",
            limit=10,
            offset=0,
        ),
    )

    response = ArticleSearchViewset.as_view({"get": "list"})(request)
    assert response.status_code is 200
    results = response.data
    import ipdb

    ipdb.set_trace()  ######## FIXME:REMOVE ME steven.joseph ################
    assert len(results["results"]) > 0
    for result in results["results"]:
        assert (
            "session_id" in result and result["session_id"] == test_session_id
        )
