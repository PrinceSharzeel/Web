from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response




from rest_framework.decorators import api_view
from pyfcm import FCMNotification
from gcm import *

@api_view(['POST'])
def notif(request):
	

	proxy_dict = {
	          "http"  : "http://http://127.0.0.1",
	          "https" : "http://http://127.0.0.1",
	        }
	push_service = FCMNotification(api_key="AIzaSyCjw01UrNb19G6acI6s2ADcShv3t4FO7Jw")

	# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging   legacy server-key


	registration_id = request.data.get("token")
	message_title = "SSUK"
	message_body = "Hi john, your customized news for today is ready"
	result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

	print(result)
	return Response({"ok":"done"})