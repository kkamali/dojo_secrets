from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'register$', views.register, name = "register"),
    url(r'login$', views.login, name = "login" ),
    url(r'secrets/(?P<user_id>\w+)/add$', views.secret_add, name = "secret_add"),
    url(r'secrets/(?P<user_id>\w+)/$', views.secret, name = "secret"),
    url(r'likes/(?P<user_id>\w+)/$', views.like, name = "like"),
    url(r'^', views.index, name = "index"),
]
