from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'test/',views.test,name='test'),
    url(r'test_page/', views.test_page, name='test_page'),
    url(r'test_page_self/', views.test_page_self, name='test_page_self')
]