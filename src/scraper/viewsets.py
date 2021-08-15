from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from src.scraper.models import Article
from src.scraper.serializers import ArticleSerializer
from src.scraper.tasks import crawl
from rest_framework.views import APIView
from rest_framework.decorators import action


class MongoSearchViewset(ListModelMixin, GenericViewSet):
    ordering = None
    limit = 10
    offset = 0

    def sort_results(self, results):
        if self.ordering:
            return sorted(
                results,
                key=lambda x: x.get(self.ordering) or "",
                reverse=self.reversed,
            )
        return results

    def list(self, request, *args, **kwargs):
        results = {}
        self.limit = int(self.request.query_params.get("limit", 10))
        self.offset = self.request.query_params.get("offset") or 0
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(context=dict(request=request))
        items = results["results"] = []
        for result in queryset:
            items.append(serializer.to_representation(result))
        results["results"] = self.sort_results(items)
        results[
            "next"
        ] = self.request.get_full_path() + "&limit=%s&offset=%s" % (
            self.limit,
            self.limit + self.offset,
        )
        results[
            "previous"
        ] = self.request.get_full_path() + "&limit=%s&offset=%s" % (
            self.limit,
            self.limit - self.offset if self.limit > self.offset else 0,
        )
        return Response(results)


class ArticleSearchViewset(MongoSearchViewset):
    serializer_class = ArticleSerializer
    ordering = "published"
    reversed = False

    def get_queryset(self):
        search_term = self.request.query_params.get("q", None)
        if search_term:
            return Article.search(search_term)
        return Article.search("*")

    @action(methods=["get"], detail=False)
    def scrape(self, request, pk=None):
        crawl.delay("theconversation")
        return Response(dict(ok=True))
