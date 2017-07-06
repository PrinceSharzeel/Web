from django.conf.urls import url,include
from . import views
from django.contrib.auth import views as auth_views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
   

url(r'^store/(?P<sname>[-\w]+)/$',views.storestatus),
    url(r'^products/(?P<uname>[\w|\W]+)/(?P<sid>[\w|\W]+)/$',views.apilist),
     url(r'^register/$',views.apireg),

     url(r'^reg/$',views.apireg2),

     url(r'^pas/$',views.apipass),
     url(r'^login/(?P<uname>[\w|\W]+)/$',views.apilogin),
	 url(r'^orders/(?P<uname>[-\w]+)/$',views.orders),

	 url(r'^orderlist/(?P<uname>[-\w]+)/$',views.orderlist),

	 url(r'^orderlist2/(?P<uname>[-\w]+)/$',views.orderlist2),
 url(r'^prod_detail/(?P<uname>[-\w]+)/$',views.Product_detail),
url(r'^order_add/$',views.add_order),

url(r'^orders/$',views.orders_items),
url(r'^category/(?P<uname>[-\w]+)/$',views.category),
url(r'^postcode/(?P<uname>[\w|\W]+)/$',views.postcode),

url(r'^date_check/(?P<uname>[-\w]+)/$',views.dateavail),

url(r'^delvat/(?P<uname>[-\w]+)/$',views.delvat),

url(r'^logo/(?P<uname>[-\w]+)/$',views.logo),

url(r'^paycard/$',views.paycard_details),

url(r'^agent_order_update/$',views.agent_delivery_details),

url(r'^invoice/(?P<shop_id>[\w|\W]+)/(?P<ord_id>[\w|\W]+)/$',views.invoice)


]


urlpatterns = format_suffix_patterns(urlpatterns)
