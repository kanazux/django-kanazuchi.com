from django.conf.urls import include, url # NOQA
from django.conf import settings # NOQA
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'galery', views.galery),
    url(r'teste', views.teste),
    url(r'ipyshow', views.ipyshow),
    url(r'ipytest', views.ipytest),
    url(r'photos', views.photos),
    url(r'familia', views.familia),
    ]
