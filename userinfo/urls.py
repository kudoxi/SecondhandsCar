from django.conf.urls import url
from . import views
from userinfo import viewUtil

urlpatterns = [
    url(r'^register/', views.register,name="register"),
    url(r'^login/', views.login,name="login"),
    url(r'^usercenter/', views.usercenter,name="usercenter"),

    url(r'^logout/', views.logout_,name="logout"),
    url(r'^dologin/', views.dologin,name="dologin"),
    url(r'^doregister/', views.doregister,name="doregister"),
    url(r'get_validcode_img/', viewUtil.get_validcode_img, name="get_validcode_img"),
    url(r'dopdf/',views.dopdf,name="dopdf"),
    url(r'email_valicode/',views.email_valicode,name="email_valicode"),
    #url(r'^get_validcode_img/', views.get_validcode_img,name="get_validcode_img"),

]