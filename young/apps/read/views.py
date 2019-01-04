from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from apps.read.serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleCommentSerializer
from apps.users.models import Article, Comment


class MyPaginateClass(PageNumberPagination):
    page_size = 15
    page_query_param = 'pn'


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.filter(is_delete=False).order_by('id').all()
    serializer_class = ArticleListSerializer
    pagination_class = MyPaginateClass
    filter_backends = [OrderingFilter]
    ordering_fields = ['update_time', 'like_count', 'read_count']

    def list(self, request, *args, **kwargs):
        response = super().list(request)
        response.data = {'data': response.data, 'code': 200}
        return response


class ArticleDetailAPIView(RetrieveAPIView):
    queryset = Article.objects.filter(is_delete=False).order_by('id').all()
    serializer_class = ArticleDetailSerializer

    def get(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = {'data': response.data, 'code': 200}
        return response


class ArticleCommentAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = ArticleCommentSerializer
    pagination_class = MyPaginateClass
    filter_backends = [OrderingFilter]
    ordering_fields = ['create_time', 'like_count']

    def get_queryset(self):
        article_id = self.request.path.split('/')[4]
        query_set = self.queryset.filter(article=article_id).all()
        return query_set

    def get(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'data': response.data, 'code': 200}
        return response
