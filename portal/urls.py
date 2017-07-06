from django.conf.urls import url,include
from . import views
from axes.decorators import watch_login
from django.contrib.auth import views as auth_views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
   url(r'^$',views.index,name='index'),
   url(r'^register/$',views.register,name='register'),
   url(r'^login/$',watch_login(views.login),name='login'),
   url(r'^logout/$',views.logout,name='logout'),
   url(r'^cp/$',views.change_password,name='cp'),
   url(r'^fg/$',views.forgot_password,name='fg'),
    url(r'^price/$',views.bulk_price,name='bulk'),
    url(r'^stock/$',views.stock,name='stock'),


   url('^', include('django.contrib.auth.urls')),
   url(r'^paypal/', include('paypal.standard.ipn.urls')),

   url(r'^home',views.home,name='home'),
   url(r'^result',views.result,name='result'),
   url(r'^single',views.product_update,name='single'),
   url(r'^pay',views.money,name='money'),

   url(r'^list',views.list,name='list'),
   url(r'^options/$', views.category, name='options'),
    url(r'^op_rem/(?P<user>[\w|\W]+)/$', views.options_remove,name='op_rem'),
   url(r'^product/(?P<user>[-\w]+)/$', views.product_update,name='product'),

   url(r'^productimage/(?P<user>[-\w]+)/$', views.prod_image,name='productimage'),
    url(r'^remove/(?P<user>[-\w]+)/$', views.product_remove,name='delete'),


   url(r'^shuto/$',views.shuto,name='so'),
   url(r'^shutc/$',views.shutc,name='sc'),

   url(r'^storestatus/$',views.storestatus,name='storestatus'),



]
