from django.shortcuts import render,render_to_response,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from pymongo import MongoClient
import random,string,imghdr,datetime
from bson.json_util import dumps

from .models import Product,Customer,Order,Cat,OrderList

from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view

from django.core.urlresolvers import reverse

import pdfkit
from reportlab.platypus import PageTemplate,SimpleDocTemplate, BaseDocTemplate, NextPageTemplate, PageBreak,Spacer,Paragraph,Table,TableStyle,Image
from reportlab.lib.units import inch

from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
from django.core.mail import EmailMultiAlternatives



from .serializers import ProductSerializer,CustomerSerializer,OrderSerializer,CatSerializer,PaycardSerializer,OrderListSerializer



client = MongoClient('localhost', 27017)
user_db= client.ssuk







@api_view(['GET'])
def storestatus(request,sname):
    if request.method == 'GET':
        
        stat=user_db.store_details.find_one({str('_id'):sname})
        
        if stat is None:
            return Response({'status':'Store not found'})
        else:
            if stat['status']=='Open':
                print('######################')
                return Response({"status" : "open"})
            else:
                stat_detail=user_db.store_status.find_one({'shop_id':sname})
                print(stat_detail)
                if stat_detail is None:

                    return Response({'status':'Closing details not found'})
                else:
                    return Response({'status':stat_detail['status'],'time':stat_detail['time'],'msg':stat_detail['msg']})













@csrf_exempt
@api_view(['GET','POST'])
def apilist(request,uname,sid):
    
    if request.method == 'GET':
        #get our collection
        products = []
        for r in user_db.product_details.find({"pcat":uname,"shop_id":sid}):
            #product = Product(r["shop_id"],r["ptitle"],r["pbrand"],r["price"],r["ppro"])

            product=Product( r["shop_id"],r['ptitle'],r['pbrand'],r['punit'],r['pcat'],r['ppro'],r['plitres'],
				        r['package'],r['pweight'],r['pdisc'],r['pmin'],r['pmax'],r['preddisc'],r['pexp'],
				        r['price'] )
            products.append(product)
        serializedList = ProductSerializer(products, many=True)
        return Response(serializedList.data)
    elif request.method == 'POST':
    
        
        shop_id = request.data.get("shop_id")
        ptitle = request.data.get("ptitle")
        pbrand=request.data.get("pbrand")
        price=request.data.get("price")
        ppro=request.data.get("ppro")
        print(request.data)
        try:user_db.product_details.insert_one({"shop_id":shop_id,"ptitle" : ptitle, "pbrand": pbrand, "ptitle":ptitle})
        except:return Response({"Ok":"false"})
        return Response({ "ok": "true" })



@api_view(['POST'])
def apireg(request):
    serialized = CustomerSerializer(data=request.data)
    if serialized.is_valid():
        password=request.data.get("password")
        contact=request.data.get("contact")
        name=request.data.get("name")
        address=request.data.get("address")
        orders=request.data.get("orders")
        postcode=request.data.get("postcode")
        email=request.data.get("email")
        u=user_db.client_users.find_one({"contact" : contact})
        if u is not None:return Response({"ok":"User Already Exist"})
        try:user_db.client_users.insert_one({'password':password,'address':address,'contact':contact,'name':name,'orders':orders,'postcode':postcode,'email':email,'agent':'No'})
        except:return Response({"ok":"false"})
        return Response({ "ok": "true" })


 
    else:
        return Response(serialized._errors)






@api_view(['POST'])
def apireg2(request):
    serialized = CustomerSerializer(data=request.data)
    if serialized.is_valid():
        password=request.data.get("password")
        contact=request.data.get("contact")
        name=request.data.get("name")
        address=request.data.get("address")
        orders=request.data.get("orders")
        email=request.data.get("email")
        
        u=user_db.client_users.find_one({"contact" :contact})
        if u is not None and u['password']==password:
            user_db.client_users.update_one(
                        {"contact":contact},
                        {
                        "$set": {'email':email,'name':name

                        }
                        },upsert=True
                    )
            
            return Response({"ok":"registered"})

       
        return Response({ "ok": "Check username or password" })



@api_view(['POST'])
def apipass(request):
    serialized = CustomerSerializer(data=request.data)
    if serialized.is_valid():
        password=request.data.get("password")
        contact=request.data.get("contact")
        name=request.data.get("name")
        address=request.data.get("address")
        orders=request.data.get("orders")
        
        postcode=request.data.get("postcode")
        email=request.data.get("email")
        u=user_db.client_users.find_one({"contact" :contact})
        if u is not None and u['password']==password:
            user_db.client_users.update_one(
                        {"contact":contact},
                        {
                        "$set": {'password':name

                        }
                        },upsert=True
                    )
            
            return Response({"ok":"Password changed"})

       
        return Response({ "ok": "Check username or password" })
    return Response("Fail")






@api_view(['GET'])
def apilogin(request,uname):
    if request.method=='GET':
        p=uname.index(' ')
        contact=uname[0:p]
        password=uname[p+1:]
        u=user_db.client_users.find_one({"contact" :uname[0:p]})
        if u is not None and u['password']==password:
            #the agent login gateway
            ag=user_db.client_users.find({"agent":{ "$exists": "true","$ne":"null"} })
            if u['agent']=='No':
                l=Customer(u['password'],u['address'],u['contact'],u['name'],u['orders'],u['postcode'],u['email'])
                serializedList=CustomerSerializer(l)
                return Response(serializedList.data)
                return Response({"Ok":"OKKK"})
            else:
                print("JHJJJJJJJJJJJJJJJJJJJJJjj")
                return Response({"agent":"ok","contact":uname[0:p]})

       
        return Response({ "name": "Check username or password" })



@api_view(['GET'])
def orders(request,uname):
    if request.method == 'GET':
        products=[]
        for r in user_db.orders.find({"contact":uname}):
            #product = Product(r["shop_id"],r["ptitle"],r["pbrand"],r["price"],r["ppro"])
            prod_detail=user_db.product_history_record.find_one({"ptitle":r['ptitle']})

            product=Product( prod_detail["shop_id"],prod_detail['pbrand'],prod_detail['punit'],prod_detail['pcat'],prod_detail['ppro'],prod_detail['plitres'],
                        prod_detail['package'],prod_detail['pweight'],prod_detail['pdisc'],prod_detail['pmin'],prod_detail['pmax'],prod_detail['preddisc'],prod_detail['pexp'],
                        prod_detail['price'] )
            products.append(product)
        if not products:return Response({"Null":"No orders"})
        serializedList = ProductSerializer(products, many=True)
        return Response(serializedList.data)





@csrf_exempt
@api_view(['GET'])
def orderlist(request,uname):
    
    if request.method == 'GET':
        #get our collection
        products = []
        for r in user_db.orders.find({"contact":uname}):
            
            print(len(r['order']))
            r_nofitems=len(r['order'])

            product=OrderList(r['_id'],r['ord_date'],r['status'],r_nofitems-1,r['total'])
            products.append(product)
        serializedList = OrderListSerializer(products, many=True)
        return Response(serializedList.data)





@csrf_exempt
@api_view(['GET'])
def orderlist2(request,uname):
    
    if request.method == 'GET':
        products = []
        try:
            orders_items=user_db.orders.find_one({"_id":ObjectId(uname)})
            print(orders_items['order'])
            if len(orders_items)==1:return Response({"ok":"You have not made any orders."})
            del_vat=orders_items['vat']+"#"+orders_items['delivery']

            for each_item,value in orders_items['order'].items():
                if value.get("name") is not None:
                    print("yes")
                    pd=user_db.product_history_record.find_one({'ptitle':value.get("name")})


                    product=OrderList(value.get("name"),value.get("price"),value.get("quant"),pd["ppro"],del_vat)
                    products.append(product)
                else:
                    print("no")

            serializedList = OrderListSerializer(products, many=True)
            return Response(serializedList.data)
        except:
            return Response({"ok":"You have not made any orders."})





@api_view(['GET'])
def Product_detail(request,uname):
    if request.method == 'GET':
        products=[]
        for r in user_db.product_history_record.find({"ptitle":uname}):
            #product = Product(r["shop_id"],r["ptitle"],r["pbrand"],r["price"],r["ppro"])

            
            sa=user_db.store_details.find_one({str("_id"):r["shop_id"]})

            product=Product( r["shop_id"],r['ptitle'],r['pbrand'],r['punit'],r['pcat'],r['ppro'],r['plitres'],
                        r['package'],r['pweight'],r['pdisc'],r['pmin'],sa['vat'],r['preddisc'],r['pexp'],
                        r['price'] )
            products.append(product)
        if not products:return Response({"Null":"No products"})
        serializedList = ProductSerializer(products, many=True)
        return Response(serializedList.data)










@api_view(['POST'])
def add_order(request):
    serialized = OrderSerializer(data=request.data)
    if serialized.is_valid():
        contact=request.data.get("contact")
        order=request.data.get("order")
        date=request.data.get("ord_date")
        address=request.data.get("ord_address")
        pay_id=request.data.get("pay_id")
        pin=request.data.get("pincode")

        time=request.data.get("ord_time")
        statuss=request.data.get("status")
        orderrrr={'null':{'null':'null'}}
        u=user_db.client_users.find_one({"contact" : contact})
        usexist=user_db.orders.find_one({"contact":contact,"status":"slotted"})
        if usexist is not None:
            user_db.orders.remove({"contact":contact,"status":"slotted"})
        if u is None:
            return Response({"fail":"Check Username or Password"})
        try:
            user_db.orders.insert({'contact':contact,'ord_date':date,'ord_address':address,'order':orderrrr,'status':statuss,'ord_time':time,'pincode':pin,'pay_id':pay_id})
        except:
            return Response({"ok":"false"})
        return Response({ "ok": "Slot Booked" })


 
    else:
        return Response(serialized._errors)




@api_view(['POST'])
def orders_items(request):
    contact=request.data.get("contact")
    name=request.data.get("ptitle")
    quant=request.data.get("quantity")
    price=request.data.get("priceunit")
    vat=request.data.get("vat")
    delivery=request.data.get("delivery")

    total=request.data.get("total")
    statuss=request.data.get("status")
    val={'name':name,'quant':quant,'price':price}
    usexist=user_db.orders.find_one({"contact":contact,"status":"slotted"})
    orderprev=usexist['order']
    orderprev[name]=val
    if usexist is not None:
        try:
            
            user_db.orders.update_one(
                        {"contact":contact,"status":"slotted"},
                        {
                        "$set": {'order':orderprev,'vat':vat,'delivery':delivery,'total':total

                        }
                        },upsert=True
                    )
            return Response({"ok":"Order placed"})
        except:
            return Response({"ok":"Please try again later"})

    else:
        return Response({"ok":"Order Not Slotted"})






















@api_view(['GET'])
def category(request,uname):
    if request.method == 'GET':
        products=[]
        for r in user_db.product_details.find({'shop_id':uname}).distinct("pcat"):
            #product = Product(r["shop_id"],r["ptitle"],r["pbrand"],r["price"],r["ppro"])
            print(r)

            product=Cat(r)
            products.append(product)
        if not products:return Response({"Null":"No category"})
        serializedList = CatSerializer(products, many=True)
        return Response(serializedList.data)

import urllib.request
import json


@api_view(['GET'])
def postcode(request,uname):
    if request.method=='GET':
        p=uname.index(' ')
        shop_id=uname[0:p]
        dest=uname[p+1:]
        print(uname[0:p])
        u=user_db.store_details.find_one({"_id" :uname[0:p]})
        if u is not None:

            origin=u['spost']
            try:
                url="https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="+origin+"&destinations="+dest
                res = urllib.request.urlopen(url).read()
                data = json.loads(res.decode())
                a=data["rows"][0]["elements"][0]["distance"]
                v=a['value']
                print(v)
                return Response(data["rows"][0]["elements"][0]["distance"])
            except:return Response({"ok":"Distance not found"})
                

       
        return Response({ "fail": "enter valid postcodes" })





@api_view(['POST'])
def paycard_details(request):
    serialized = PaycardSerializer(data=request.data)
    if serialized.is_valid():
        contact=request.data.get("contact")
        date=request.data.get("date")
        name=request.data.get("name")
        nick=request.data.get("nick")
        ctype=request.data.get("ctype")
        number=request.data.get("number")
        bill_add=request.data.get("bill_addr")
        u=user_db.client_users.find_one({"contact" : contact})
        uexist=user_db.payment_cards.find_one({"contact":contact})
        if uexist is not None:user_db.payment_cards.remove({"contact":contact})
        if u is None:return Response({"fail":"Check Username or Password"})
        user_db.payment_cards.remove({'contact':contact})
        try:user_db.payment_cards.insert({'contact':contact,'date':date,'name':name,'nick':nick,'ctype':ctype,'bill_addr':bill_add,'number':number})
        except:return Response({"ok":"false"})
        pid=str(user_db.client_users.find_one({"contact" : contact})["_id"])
        return Response({ "ok":pid})


 
    else:
        return Response(serialized._errors)









@api_view(['POST'])
def agent_delivery_details(request):
    contact=request.data.get("contact")
    oid=request.data.get("oid")
    stat=request.data.get("stat")
    feed=request.data.get("feed")
    print(oid)
    uexist=user_db.orders.find_one({"_id":ObjectId(oid)})
    print(uexist)
    if uexist is not None:
        try:
            
            user_db.orders.update_one(
                        {"_id":ObjectId(oid)},
                        {
                        "$set": {'status':stat,'feedback':feed,'agent':contact

                        }
                        },upsert=True
                    )
            return Response({"ok":"Order status updated"})
        except:
            return Response({"ok":"Please try again later"})
        
    return Response({ "ok":"error"})


 











@api_view(['GET'])
def dateavail(request,uname):
    if request.method=='GET':
        u=user_db.store_details.find_one({"_id" :uname})
        if u is not None:

            return Response({"wdstop":u['wdstop'],"wdstart":u['wdstart'],"wstop":u['wstop'],"wstart":u['wstop']})
            

       
        return Response({ "fail": "Null" })



@api_view(['GET'])
def delvat(request,uname):
    if request.method=='GET':
        u=user_db.store_details.find_one({"_id" :uname})
        if u is not None:

            return Response({"vat":u['vat'],"del_char":u['delchr']})
            

       
        return Response({ "fail": "Null" })




@api_view(['GET'])
def logo(request,uname):
    if request.method=='GET':
        u=user_db.store_details.find_one({"_id" :uname})
        if u is not None:

            return Response({"pic":u['flogo'],"name":u['sname']})
            

       
        return Response({ "fail": "Null" })





def mail_pdf(request,attachment,contact,mail,oid,tomail):
    subject = 'Welcome to Project Management Portal.'
    message = 'Please find the soft copy of the invoice for order '+oid+' attached for your reference. Thank you for shopping!\n Regards\nContact Us: '+str(contact)+' \n '+str(mail)
    from_email = settings.EMAIL_HOST_USER
    to_list = [tomail, settings.EMAIL_HOST_USER]
    message = EmailMultiAlternatives(subject, message, from_email, to_list)
    message.attach_file(attachment)
    message.send()    
    #messages.add_message(request, messages.INFO, 'Invoice Mailed Successfully !!')
    print("Done")
    return 1

from reportlab.lib import colors
from  reportlab.lib.styles import ParagraphStyle as PS

import os

@api_view(['GET'])
def invoice(request,shop_id,ord_id):
    if request.method=='GET':
        ord_items=user_db.orders.find_one({'_id':ObjectId(ord_id)})
        if ord_items is None:
            return Response({'ok':'No orders Found'})
        else:
            attachment="static/media/invoices/invoice_"+str(ord_items['_id'])[-10:]+".pdf"
            doc = SimpleDocTemplate(attachment, rightMargin=72, leftMargin=72, topMargin=-70)
            styles = getSampleStyleSheet()
            Story = [Spacer(1, 2 * inch)]
            h1 = PS(
                name = 'Heading1',
                fontSize = 14,
                leading = 16)


            h2 = PS(name = 'Heading2',
                fontSize = 12,
                leading = 14)

            shop=user_db.store_details.find_one({'_id':shop_id})
            name_client=user_db.client_users.find_one({'contact':ord_items['contact']})
            Story.append(Paragraph("INVOICE", h1))
            Story.append(Paragraph("Company Name : "+str(shop['sname']),h1))
            comp_details="Address : "+str(shop['sadd1'])+" , "+str(shop['sadd2'])+" , "+str(shop['scity'])+" , "+str(shop['spost']) 
            Story.append(Paragraph(comp_details , h2))

            Story.append(Paragraph("Order number : "+str(ord_items['_id'])[-10:], h2))

            Story.append(Paragraph("Ordered By : "+str(name_client['name']).replace('#',' '), h2))
            Story.append(Paragraph("Order Details :", h2))

            style = styles["Normal"]
            l=[]
            l.append(["Item","Quantity  ( units )","Cost / unit ( in € )   ","Total"])

            for each_item,value in ord_items['order'].items():
                if value.get("name") is not None:
                    print("yes")
                    l.append([value.get("name"),value.get("quant"),value.get("price"),float(value.get('price'))*float(value.get('quant'))])
                else:
                    print("no")


            
            t=Table(l,5*[1.25*inch], len(l)*[0.25*inch])

            t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'CENTER'),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))

            Story.append(t)
            Story.append(Paragraph("", h2))
            Story.append(Paragraph("", h2))
            if ord_items['ord_address']!='not':
                Story.append(Paragraph("Delivery Address: "+str(ord_items['ord_address']), h2))
            else:
                Story.append(Paragraph("Picked at Shop", h2))
            Story.append(Paragraph("", h2))

  


            Story.append(Paragraph("Delivery Date : "+str(ord_items['ord_date']), h2))

            Story.append(Paragraph("VAT : "+str(ord_items['vat'])+" %", style))

            Story.append(Paragraph("Total Price : € "+str(ord_items['total']), h1))

            paratext=('*Terms and Conditions apply as per Store Policy')
            p = Paragraph(paratext, style)
            Story.append(p)
            Story.append(Spacer(1, 0.2 * inch))
            doc.build(Story)
            #find users mail
            user_mail=user_db.client_users.find_one({'contact':ord_items['contact']})

            mail_pdf(request,attachment,shop['cont'],shop['smail'],str(ord_items['_id'])[-10:],user_mail['email'])
            a={'ok':'Invoice has been Mailed'}
            return Response(a)


