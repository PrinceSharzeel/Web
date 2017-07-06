from django.shortcuts import render,render_to_response,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .forms import RegistrationForm,LoginForm,Password_Change,StoreForm,ProductForm,ProductNewForm,CatForm,ImageForm,StoreStatusForm
from django.contrib import messages
from django.template import RequestContext
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from pymongo import MongoClient
import random,string,imghdr,datetime
from axes.decorators import watch_login
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from bson.json_util import dumps


from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt


from django.core.urlresolvers import reverse





client = MongoClient('localhost', 27017)
user_db= client.ssuk



watch_login
def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if(request.method=='POST'):
		l_form=LoginForm(request.POST)
		if l_form.is_valid():

			email = l_form.cleaned_data['fail']
			psd= l_form.cleaned_data['fswd']
			user = authenticate(username=email,password=psd)
			if user is not None:
				auth_login(request,user)
				u=user_db.users_details.find_one({"email" : email})
				messages.success(request,'Hello'+' '+u['fname'])
				return HttpResponseRedirect('/')
			else:
				messages.error(request,'Email or Password incorrect')
				return HttpResponseRedirect('/login')

		messages.error(request,'Fill the form correctly')
		return render(request,'login.html',{'l_form':l_form})
	l_form=LoginForm()
	return render(request,'login.html',{'l_form':l_form})










@login_required(login_url='/login/')
def index(request):
	if request.method=='POST':
		form=StoreForm(request.POST,request.FILES)


		if form.is_valid():
			if 'flogo' in request.FILES:
				url = image(request.FILES['flogo'],"shop"+request.POST['fsname'])
				if url==0:	
					messages.error(request,"Not an image")
					return HttpResponseRedirect(request,'/login/')
				picture_url=url;
			else:
				picture_url="/static/media/default.png"




			if 'policy' in request.FILES:
				policy_name=file_save(request.FILES['policy'],request.POST['fsname'])
			else:
				messages.error(request,"Wrong File")
				return HttpResponseRedirect(request,'/')





			#messages.success(request, 'Successfully registered. Please Login')
			#return HttpResponse('in')
  
			request.session["_id"] = str(user_db.users_details.find_one({"email" : request.user.username})["_id"])
			answer = request.POST.get('fcat',False)
			sname=form.cleaned_data['fsname']
			vat=form.cleaned_data['fvat']
			cid=form.cleaned_data['fid']
			scity=form.cleaned_data['fcity']
			sadd1=form.cleaned_data['fadd1']
			sadd2=form.cleaned_data['fadd2']
			spost=form.cleaned_data['fpostcode']
			scountry=form.cleaned_data['fcountry']
			state=form.cleaned_data['fstate']
			smail=form.cleaned_data['fsmail'] 
			sweb=form.cleaned_data['fweb']
			cat=request.POST['fcat']
			cont=form.cleaned_data['fcont']
			wstart=form.cleaned_data['wstart']
			wstop=form.cleaned_data['wstop']
			wstart=str(wstart)
			wstop=str(wstop)

			wdstart=form.cleaned_data['wdstart']
			wdstop=form.cleaned_data['wdstop']
			wdstart=str(wdstart)
			wdstop=str(wdstop)
			user_data = user_db.store_details.find_one({"_id":request.session["_id"]})
			if user_data is None:
				entry={'sname':sname,'vat':vat,'cid':cid,'scity':scity,'sadd1':sadd1,'sadd2':sadd2,'spost':spost,'scountry':scountry,'state':state,'smail':smail,'sweb':sweb,'policy':policy_name,'status':'Open','cat':request.POST['fcat'],'cont':cont,'flogo':picture_url,'wstart':wstart,'wstop':wstop,'wdstart':wdstart,'wdstop':wdstop}
				user_db.store_details.insert(entry)
			else:
				user_db.store_details.update_one(
					        {"_id": request.session["_id"]},
					        {
					        "$set": {'sname':sname,'vat':vat,'cid':cid,
				        'scity':scity,'sadd1':sadd1,'sadd2':sadd2,'spost':spost,
				        'scountry':scountry,
				        'state':state,
				        'smail':smail,'sweb':sweb,'policy':policy_name,
				        'cat':request.POST['fcat'],'cont':cont,'flogo':picture_url,'wstart':wstart,'wstop':wstop,'wdstart':wdstart,'wdstop':wdstop,

					        }
					        },upsert=True
					    )
			user_data = user_db.store_details.find_one({"_id":request.session["_id"]})

			entry={'sname':user_data['sname'],'vat':user_data['vat'],'cid':user_data['cid'],
			        'scity':user_data['scity'],'sadd1':user_data['sadd1'],'sadd2':user_data['sadd2'],'spost':user_data['spost'],
			        'scountry':user_data['scountry'],
			        'state':user_data['state'],'policy':user_data['policy'],
			        'smail':user_data['smail'],'sweb':user_data['sweb'],'flogo':user_data['flogo'],'status':user_data['status'],
			        'cat':user_data['cat'],'cont':user_data['cont'],'wstart':user_data['wstart'],'wstop':user_data['wstop'],'wdstart':user_data['wdstart'],'wdstop':user_data['wdstop']}

			option_list= user_db.category_items.find({"shop_id":request.session["_id"]})
			messages.success(request,"Saved")
			return render(request,'Signup.html',{'form':entry,'options':option_list})

		
		





		else:
			messages.error(request,'Fill the Details Correctly')
			return HttpResponseRedirect('/')
			#return HttpResponse(form.errors)
	
	






	else:
		request.session["_id"] = str(user_db.users_details.find_one({"email" : request.user.username})["_id"])
		#return HttpResponse(request.session)
		option_list= user_db.category_items.find({"shop_id":request.session["_id"]})
		#user_detail = user_db..find({"shop_id":ObjectId(request.session["_id"])})
		#option_list = user_db.category_items.find(str(user_db.users_details.find_one({"email" : request.user.username})["_id"]))


		user_data = user_db.store_details.find_one(str(user_db.users_details.find_one({"email" : request.user.username})["_id"]))

		
		if user_data is not None:
			dicto={'sname':user_data['sname'],'sadd1':user_data['sadd1'],'sadd2':user_data['sadd2'],'spost':user_data['spost'],'scity':user_data['scity'],'cat':user_data['cat'],'cont':user_data['cont'],'scountry':user_data['scountry'],
			'smail':user_data['smail'],'sweb':user_data['sweb'],'status':user_data['status'],'cid':user_data['cid'],'vat':user_data['vat'],'flogo':user_data['flogo'],'state':user_data['state'],'wstart':user_data['wstart'],'wstop':user_data['wstop'],'wdstart':user_data['wdstart'],'wdstop':user_data['wdstop']}
			return render(request,'Signup.html',{'form':dicto,'options':option_list})
		dicto={'status':'Open','reged':'no'}
		return render(request,'Signup.html',{'form':dicto})

			
		



def file_save(f,i):

	path = "static/policy/"+i
	try:
		with open(path, 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)		
	except:
		return "/static/policy/default.doc"
	return "/static/policy/"+i








def register(request):

	if request.method=='POST':
		form=RegistrationForm(request.POST)
		
		if form.is_valid():
			firstName = form.cleaned_data['ffname']
			lastName = form.cleaned_data['flname']
			email = form.cleaned_data['fmail']
			password=form.cleaned_data['fpswd']
			cpassword=form.cleaned_data['fcpswd']
			if password==cpassword:
				entry={'fname':firstName,'lname':lastName,'email':email}
				user_db.users_details.insert_one(entry)
				User.objects.create_user(username=entry["email"],email=entry["email"],password=password)
				messages.success(request,'Successfully registered, You can now login!!!')

				return HttpResponseRedirect('/login/')

			else:
				messages.error(request,'Passwords do not match')
				return render(request,'login.html')
		
		messages.error(request,'Fill the form collectly')
		return render(request,'login.html')
	form=RegistrationForm()
	return render(request,'login.html')



def logout(request):
	u=request.user
	if request.user.is_authenticated():
		auth_logout(request)
		return HttpResponseRedirect("/login/")
	else:
		return HttpResponseRedirect('/login/')





@login_required(login_url='/login/')		
def change_password(request):
	if request.method == 'POST':
		form=Password_Change(request.POST)
		use_cp= request.user
		#return HttpResponse(use_cp)
		

		if form.is_valid() and request.POST['new_password']==request.POST['retype_password']:
			
			
			if use_cp.check_password(request.POST['current_password']):
				
				
				if len(request.POST['new_password'])<5:
					messages.error(request,'New password must be at least 5 characters long.')
					return HttpResponseRedirect("/cp/")

				if request.POST['current_password']==request.POST['new_password']:
					messages.error(request,'Choose a new password.')
					return HttpResponseRedirect("/cp/")


				

				use_cp.set_password(request.POST['new_password'])
				messages.success(request,"Password change successful. Please login again with new password.")
				use_cp.save()
				return HttpResponseRedirect('/login/')
			else:
				messages.error(request,'Old password is wrong.')
				return HttpResponseRedirect("/cp/")
		else:
			messages.error(request,'Passwords do not match.')
			return HttpResponseRedirect("/cp/")

	form=Password_Change()
	return render(request,'fg.html',{'form':form})








def forgot_password(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.method=='POST':
		if 'email' in request.POST and request.POST['email']:
			try:
				u=user_db.users_details.find_one({"email" : request.POST['email']})
			except:
				messages.error(request,'Email not registered')
				return HttpResponseRedirect('/login/')
			
			code=''.join(random.SystemRandom().choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for _ in range(20))
			
			url="http://malaviyans.online/reset/?email="+u['email']+"&user="+u['fname']+"&code="+code
			try:
				send_mail('Password Reset Link', 'Please follow this link to reset your password: '+url, 'alumni@malaviyans.online',[u['email']], fail_silently=False)
			except:
				messages.error(request,'Some error occured. Please try again later.')
				return HttpResponseRedirect('/login/')
			else:
				messages.success(request,' A reset link has been sent to your email. Please follow it to reset your password.')
				return HttpResponseRedirect('/login/')
	return HttpResponseRedirect('/login')
			


				
def image(f,i):
	ext = imghdr.what(f)
	if ext in ['jpeg','png','bmp']:
		a=''.join(random.SystemRandom().choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for _ in range(3))
		
		path = "static/media/"+i+"."+ext
		try:
			with open(path, 'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
		except:
			return "/static/media/default.png"
		return "/static/media/"+i+"."+ext
	else:
		return 0;








@login_required(login_url='/home')
def home(request):

	
	if request.method=='POST':
		form=ProductForm(request.POST,request.FILES)

		if form.is_valid():
			if 'ppro' in request.FILES:
				url = image(request.FILES['ppro'],request.POST['ptitle'])
				if url==0:	
					messages.error(request,"Not an image")
					return HttpResponseRedirect(request,'/home/')
				picture_url=url;
			else:
				picture_url="/static/postad/default.png"
  
			request.session["_id"] = str(user_db.users_details.find_one({"email" : request.user.username})["_id"])
			answer = request.POST.get('pcat',False)


			






			user_db.product_history_record.update_one(
				        {"ptitle": request.POST["ptitle"]},
				        {
				        "$set": {'shop_id':request.session["_id"],'ptitle':form.cleaned_data['ptitle'],'pbrand':form.cleaned_data['pbrand'],'punit':form.cleaned_data['punit'],'pcat':answer,'ppro':picture_url,'plitres':form.cleaned_data['plitres'],
				        'package':form.cleaned_data['package'],'pweight':form.cleaned_data['pweight'],'pdisc':form.cleaned_data['pdisc'],'pmin':form.cleaned_data['pmin'],'pmax':form.cleaned_data['pmax'],'preddisc':form.cleaned_data['preddisc'],'pexp':form.cleaned_data['pexp'],
				        'price':form.cleaned_data['price'],'pexp':form.cleaned_data['pexp']

				        }
				        },upsert=True
				    )

			user_db.product_details.update_one(
				        {"ptitle": request.POST["ptitle"]},
				        {
				        "$set": {'shop_id':request.session["_id"],'ptitle':form.cleaned_data['ptitle'],'pbrand':form.cleaned_data['pbrand'],'punit':form.cleaned_data['punit'],'pcat':answer,'ppro':picture_url,'plitres':form.cleaned_data['plitres'],
				        'package':form.cleaned_data['package'],'pweight':form.cleaned_data['pweight'],'pdisc':form.cleaned_data['pdisc'],'pmin':form.cleaned_data['pmin'],'pmax':form.cleaned_data['pmax'],'preddisc':form.cleaned_data['preddisc'],'pexp':form.cleaned_data['pexp'],
				        'price':form.cleaned_data['price'],'pexp':form.cleaned_data['pexp']

				        }
				        },upsert=True
				    )




			user_data = user_db.product_details.find_one({"ptitle": request.POST["ptitle"]})




			i = datetime.datetime.now()
			if user_data['punit']<=50:reorder="Yes"
			else: reorder="No"

			price_entry={'shop_id':request.session["_id"],'ptitle':form.cleaned_data['ptitle'],'price':form.cleaned_data['price'],'time':str(i),'product_id':user_data['_id']}
			

			user_db.price_record.insert_one(price_entry)

			stock={'shop_id':request.session["_id"],'ptitle':form.cleaned_data['ptitle'],'cost':form.cleaned_data['price'],'date':str(datetime.datetime.now()),'product_id':user_data['_id'],'reorder':reorder,'reorder_level':50,'unit':user_data['punit']}
			

			user_db.stock_details.insert_one(stock)


			#return HttpResponse('yaha hunj')
			entry={'ptitle':user_data['ptitle'],'pbrand':user_data['pbrand'],'punit':user_data['punit'],'pcat':user_data['pcat'],'ppro':picture_url,'plitres':user_data['plitres'],
				        'package':user_data['package'],'pweight':user_data['pweight'],'pdisc':user_data['pdisc'],'pmin':user_data['pmin'],'pmax':user_data['pmax'],'preddisc':user_data['preddisc'],'pexp':user_data['pexp'],
				        'price':user_data['price'],'pexp':user_data['pexp']}



       
			request.session['product_name']=user_data['ptitle']
			messages.success(request,"Product added successfully. Go to My Products to Check")
			return render(request,'add_product.html',{'form':entry})
		





		else:
			
			messages.error(request,'Fill the Details Correctly, with proper field values and size.')
			return HttpResponseRedirect('/home')






	form=ProductForm()
	option_list= user_db.category_items.find({"shop_id":request.session["_id"]})
	return render(request,'add_product.html',{'form':form,'options':option_list})


def result(request):
	user_data = user_db.store_details.find_one(str(user_db.users_details.find_one({"email" : request.user.username})["_id"]))
		
	if user_data is not None:
			dicto={'sname':user_data['sname'],'sadd1':user_data['sadd1'],'sadd2':user_data['sadd2'],'spost':user_data['spost'],'scity':user_data['scity'],'cat':user_data['cat'],'cont':user_data['cont'],'scountry':user_data['scountry'],
			'smail':user_data['smail'],'sweb':user_data['sweb'],'cid':user_data['cid'],'vat':user_data['vat'],'flogo':user_data['flogo'],'state':user_data['state'],'wstart':user_data['wstart'],'wstop':user_data['wstop'],'wdstart':user_data['wdstart'],'wdstop':user_data['wdstop']}
			return render(request,'all-classifieds.html',{'form':dicto})
	#return render(request,'all-classifieds.html')

	





def list(request):
	product_list= user_db.product_details.find({"shop_id":request.session["_id"]})
	#return HttpResponse(product_list['pmax'])	
	if product_list is not None:
			return render(request,'products.html',{'result':product_list})
   
	return render(request,'products.html')


def prod_image(request,user):
	if request.method=='POST':
		form=ImageForm(request.POST,request.FILES)


		if form.is_valid():

			print("validated")
			if 'ppro' in request.FILES:
				url = image(request.FILES['ppro'],user)
				if url==0:	
					messages.error(request,"Not an image")
					return HttpResponseRedirect(request,'/product/user')
				picture_url=url;
			else:
				picture_url="/static/postad/default.png"
			product_name=user
			print("saveeed")

			request.session["_id"] = str(user_db.users_details.find_one({"email" : request.user.username})["_id"])
			user_db.product_history_record.update_one(
				        {"ptitle": product_name},
				        {
				        "$set": {'ppro':picture_url
				        }
				        },upsert=True
				    )

			user_db.product_details.update_one(
				        {"ptitle": product_name},
				        {
				        "$set": {'ppro':picture_url

				        }
				        },upsert=True
				    )
			print("succeded")
			user_data = user_db.product_details.find_one({"ptitle": user})
			option_list= user_db.category_items.find({"shop_id":request.session["_id"]})
				    


   

			
			#return HttpResponse('yaha hunj')
			entry={'ptitle':user_data['ptitle'],'pbrand':user_data['pbrand'],'punit':user_data['punit'],'pcat':user_data['pcat'],'plitres':user_data['plitres'],
				        'package':user_data['package'],'pweight':user_data['pweight'],'pdisc':user_data['pdisc'],'pmin':user_data['pmin'],'pmax':user_data['pmax'],'preddisc':user_data['preddisc'],'pexp':user_data['pexp'],
				        'price':user_data['price'],'pexp':user_data['pexp'],'ppro':user_data['ppro']}




       

			
			messages.success(request,"Product Image Updated Successfully.")
			return render(request,'product_new.html',{'form':entry,'options':option_list})
		





		else:
			print(form.errors)
			
			messages.error(request,'Unknown File Input')
			return HttpResponseRedirect('')





	else:
		print("JNKJNKJNKJBNKBKBNKBJ")

		
		product_name=user
		product_data = user_db.product_details.find_one({"ptitle":product_name})
		print("dkjsnkjdnskjdnkj")
		
		if product_data is not None:
			entry={'ppro':product_data['ppro']}
			print(entry)
			return render(request,'product_new.html',{'prof':entry})
		return render(request,'product_new.html')



















@login_required(login_url='/home')
def product_update(request,user):
	
	if request.method=='POST':
		form=ProductNewForm(request.POST)

		if form.is_valid():
			
			product_name=user

			request.session["_id"] = str(user_db.users_details.find_one({"email" : request.user.username})["_id"])
			answer = request.POST.get('pcat',False)
			ptitle=form.cleaned_data['ptitle']

			user_db.product_history_record.update_one(
				        {"ptitle": product_name},
				        {
				        "$set": {'shop_id':request.session["_id"],'ptitle':form.cleaned_data['ptitle'],'pbrand':form.cleaned_data['pbrand'],'punit':form.cleaned_data['punit'],'pcat':answer,'plitres':form.cleaned_data['plitres'],
				        'package':form.cleaned_data['package'],'pweight':form.cleaned_data['pweight'],'pdisc':form.cleaned_data['pdisc'],'pmin':form.cleaned_data['pmin'],'pmax':form.cleaned_data['pmax'],'preddisc':form.cleaned_data['preddisc'],'pexp':form.cleaned_data['pexp'],
				        'price':form.cleaned_data['price'],'pexp':str(form.cleaned_data['pexp'])

				        }
				        },upsert=True
				    )

			user_db.product_details.update_one(
				        {"ptitle": product_name},
				        {
				        "$set": {'shop_id':request.session["_id"],'ptitle':form.cleaned_data['ptitle'],'pbrand':form.cleaned_data['pbrand'],'punit':form.cleaned_data['punit'],'pcat':answer,'plitres':form.cleaned_data['plitres'],
				        'package':form.cleaned_data['package'],'pweight':form.cleaned_data['pweight'],'pdisc':form.cleaned_data['pdisc'],'pmin':form.cleaned_data['pmin'],'pmax':form.cleaned_data['pmax'],'preddisc':form.cleaned_data['preddisc'],'pexp':form.cleaned_data['pexp'],
				        'price':form.cleaned_data['price'],'pexp':str(form.cleaned_data['pexp'])

				        }
				        },upsert=True
				    )

			






			i = datetime.datetime.now()
			user_data = user_db.product_details.find_one({"ptitle": request.POST["ptitle"]})
			


			user_stock= user_db.stock_details.find_one({"ptitle": product_name})
			if int(user_data['punit'])<=int(user_stock['reorder_level']):reorder="Yes"
			else:reorder='No'
			user_db.stock_details.update_one(
				        {"ptitle": product_name},
				        {
				        "$set": {'shop_id':request.session["_id"],'ptitle':form.cleaned_data['ptitle'],'cost':form.cleaned_data['price'],
				        'date':str(datetime.datetime.now()),'product_id':user_data['_id'],'reorder':reorder,'reorder_level':50,'unit':user_data['punit']
				        }
				        },upsert=True
				    )
			


 
			price_entry={'shop_id':request.session["_id"],'ptitle':form.cleaned_data['ptitle'],'price':form.cleaned_data['price'],'time':i,'product_id':user_data['_id']}
			user_db.price_record.insert_one(price_entry)
			option_list= user_db.category_items.find({"shop_id":request.session["_id"]})
				    


   

			
			#return HttpResponse('yaha hunj')
			entry={'ptitle':user_data['ptitle'],'pbrand':user_data['pbrand'],'punit':user_data['punit'],'pcat':user_data['pcat'],'plitres':user_data['plitres'],
				        'package':user_data['package'],'pweight':user_data['pweight'],'pdisc':user_data['pdisc'],'pmin':user_data['pmin'],'pmax':user_data['pmax'],'preddisc':user_data['preddisc'],'pexp':user_data['pexp'],
				        'price':user_data['price'],'pexp':user_data['pexp'],'ppro':user_data['ppro']}




       

			messages.success(request,"Product Updated Successfully.")
			return render(request,'product_new.html',{'form':entry,'options':option_list})
		





		else:
			
			messages.error(request,'Fill the Details Correctly')
			return HttpResponseRedirect('product')





	else:
		product_name=user
		product_data = user_db.product_details.find_one({"ptitle":product_name})
		option_list= user_db.category_items.find({"shop_id":request.session["_id"]})
		
		if product_data is not None:
			entry={'ptitle':product_data['ptitle'],'pbrand':product_data['pbrand'],'punit':product_data['punit'],'pcat':product_data['pcat'],'plitres':product_data['plitres'],
				        'package':product_data['package'],'pweight':product_data['pweight'],'pdisc':product_data['pdisc'],'pmin':product_data['pmin'],'pmax':product_data['pmax'],'preddisc':product_data['preddisc'],'pexp':product_data['pexp'],
				        'price':product_data['price'],'pexp':product_data['pexp'],'ppro':product_data['ppro']}
			return render(request,'product_new.html',{'form':entry,'options':option_list})
		return render(request,'product_new.html')

			










def bulk_price(request):
    #If request method is POST, update the database 
    if request.method == "POST":
    	print(request.POST)
    	for key in request.POST: #Iterate through POST variables
            value = request.POST[key]
            try:
                objectId = ObjectId(key)
            except Exception as e:
                #The key is not a valid object id, it might be csrfmiddlewaretoken or some other post data
                #print(e)
                continue
            user_db.product_details.update_one(
				        {"_id": objectId},
				        {
				        "$set": {'price':value
				        }
				        },upsert=True

				    )

    #Render the update price page         
    product_list= user_db.product_details.find({"shop_id":request.session["_id"]})
    user_data = user_db.store_details.find_one({"_id":request.session["_id"]})
    if product_list is not None:
            return render(request,'price.html',{'result':product_list,'status':user_data['status']})
    return render(request,'price.html')






def stock(request):
    if request.method == "POST":
    	print(request.POST)
    	for key in request.POST: #Iterate through POST variables
            value = request.POST[key]
            try:
                objectId = ObjectId(key)
            except Exception as e:
                #The key is not a valid object id, it might be csrfmiddlewaretoken or some other post data
                #print(e)
                continue
            user_db.stock_details.update_one(
				        {"_id": objectId},
				        {
				        "$set": {'reorder_level':value
				        }
				        },upsert=True)
            
            u= user_db.stock_details.find_one({"_id":objectId})
            if u['unit']<int(u['reorder_level']):
                utt="Yes"
            else:
                utt="No"
            user_db.stock_details.update_one(
				        {"_id": objectId},
				        {
				        "$set": {'reorder':utt
				        }
				        },upsert=True)
            messages.success(request,"Success")
            

    product_list= user_db.stock_details.find({"shop_id":request.session["_id"]})
	#return HttpResponse(product_list['pmax'])
    if product_list is not None:
        return render(request,'stock.html',{'result':product_list})
    return render(request,'stock.html')






def category(request):

	if request.method=='POST':
		form=CatForm(request.POST)
		if form.is_valid():
			entry={'fname':form.cleaned_data['cat'],'shop_id':request.session['_id']}

			user_db.category_items.insert_one(entry)
			messages.success(request,"Option added")
			return HttpResponseRedirect('/options')

		else:
			messages.error(request,"Invalid Option")
			return HttpResponseRedirect('/options')
	
	option_list= user_db.category_items.find({"shop_id":request.session["_id"]})
	
	form=CatForm()

	user_data = user_db.store_details.find_one({"_id":request.session["_id"]})

	return render(request,'options.html',{'result':option_list,'form':form,'status':user_data['status']})
	#return render(request,'options.html')


def options_remove(request,user):
	user_db.category_items.remove({"fname":user})
	return HttpResponseRedirect('/options')














#product removal

def product_remove(request,user):
	user_db.product_details.remove({"ptitle":user})
	return HttpResponseRedirect('/list')

def permanent_remove(request,user):
	user_db.product_details.remove({"ptitle":user})
	user_db.product_history_record.remove({"ptitle":user})
	return HttpResponseRedirect('/list')




  #store shut open or close

def shuto(request):
	db_exist= user_db.store_details.find({"_id":request.session["_id"]})
	if db_exist is None:
		messages.errors("Register Your Store First")
		return HttpResponseRedirect('/login')
	user_db.store_details.update_one(
				        {"_id": request.session["_id"]},
				        {
				        "$set": {'status':'Open'
				        }
				        },upsert=True

				    )
	return HttpResponseRedirect('/')

def shutc(request):
	db_exist= user_db.store_details.find({"_id":request.session["_id"]})
	if db_exist is None:
		messages.errors("Register Your Store First")
		return HttpResponseRedirect('/login')
	user_db.store_details.update_one(
				        {"_id": request.session["_id"]},
				        {
				        "$set": {'status':'Closed'
				        }
				        },upsert=True
				    )
	return HttpResponseRedirect('/')





def storestatus(request):
	if request.method=='POST':
		form=StoreStatusForm(request.POST)
		if form.is_valid():
			print("validdddddddddddd")


			time=form.cleaned_data['ftime']
			msg=form.cleaned_data['fmsg']
			user_db.store_details.update_one(
					        {"_id": request.session["_id"]},
					        {
					        "$set": {'status':'Closed'
					        }
					        },upsert=True
					    )


			db_exist= user_db.store_status.find_one({"shop_id":request.session["_id"]})
			entry={'status':'Closed','time':time,'msg':msg,'shop_id':request.session["_id"]}
			if db_exist is not None:
				user_db.store_status.remove({"shop_id":request.session["_id"]})
				user_db.store_status.insert(entry)
			else:
				user_db.store_status.insert(entry)
			db_exit= user_db.store_status.find_one({"shop_id":request.session["_id"]})
			return render(request,'storestatus.html',{'status':db_exit['status']})


		else:
			db_exit= user_db.store_details.find_one({"_id":request.session["_id"]})
			return render(request,'storestatus.html',{'status':db_exit['status']})





	else:

		db_exit= user_db.store_details.find_one({"_id":request.session["_id"]})
		if db_exit is None:
			return render(request,'storestatus.html',{'status':'Open'})

		return render(request,'storestatus.html',{'status':db_exit['status']})




















def money(request):

    # What you want the button to do.

    request.session['order_id']=request.session['_id']
    return redirect(reverse('payment:process'))


















