from . import views

from django.conf.urls import url

urlpatterns = [
    url('^articles/list$', views.ArticleListAPIView.as_view()),
    url('^articles/detail/(?P<pk>\d+)$', views.ArticleDetailAPIView.as_view()),
    url('^articles/detail/(?P<pk>\d+)/comments$', views.ArticleCommentAPIView.as_view()),
    # url('^articles/detail/(?P<pk>\d+)/sub_comment/(?P<comment_id>\d+)$', views.ArticleCommentAPIView.as_view())
]
