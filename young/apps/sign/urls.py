from . import views

from django.conf.urls import url

urlpatterns = [
    url('^register$', views.RegisterAPIView.as_view()),
    url('^sign_pwd', views.SignInAPIView.as_view()),
    url('^sign_sms', views.SignInAPIView.as_view()),
    url('^send_sms/(?P<mobile>1[345789]\d{9})', views.SendSms.as_view()),
]
