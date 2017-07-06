from django.conf.urls import url,include
from . import views
from django.contrib.auth import views as auth_views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
   

    url(r'^send/$',views.notif),


]


urlpatterns = format_suffix_patterns(urlpatterns)

