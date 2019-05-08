from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$', IdexView.index,name="index"),
    url(r'test2/', IdexView.test2,name="test2"),
]