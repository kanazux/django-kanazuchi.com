from django.conf.urls import include, url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'galery', views.galery),
    url(r'teste', views.teste),
    url(r'about', views.about),
    url(r'fogonorabo', views.fogonorabo),
    url(r'tarik', views.tarik),
    url(r'familia', views.familia),
    url(r'spdsw', views.spdsw),
    ]
