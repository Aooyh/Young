from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView

from apps.users.models import Article
from apps.write.serializers import ArticleSerializer


class ArticleAPIView(CreateAPIView, UpdateAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'data': response.data, 'code': 200}
        return response

    def put(self, request, *args, **kwargs):
        response = super().update(request)
        response.data = {'data': response.data, 'code': 200}
        return response
