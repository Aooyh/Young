from django.conf.urls import url

from . import views

urlpatterns = {
    url(r'^article/(?P<pk>\d*)$', views.ArticleAPIView.as_view())
}
