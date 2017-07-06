from django.db import models


class Product(object):
    def __init__(self, shop_id ,ptitle, pbrand,punit,pcat,ppro,plitres,package,pweight,pdisc,pmin,pmax,preddisc,pexp,price):
        self.shop_id = shop_id
        self.ptitle = ptitle
        self.pbrand = pbrand
        self.punit=punit
        self.pcat=pcat
        self.ppro=ppro
        self.plitres=plitres
        self.pmin=pmin
        self.pmax=pmax
        self.preddisc=preddisc
        self.pdisc=pdisc
        self.plitres=plitres
        self.pweight=pweight
        
        self.package=package
        self.price=price
        self.pexp=pexp

	


class Customer(object):
    def __init__(self,password,address,contact,name,orders,postcode,email):
        self.password=password
        self.address=address
        self.contact=contact
        self.name=name
        self.orders=orders
        self.postcode=postcode
        self.email=email

class Order(object):
	def __init__(self,contact,order,ord_date,ord_address,ord_time,pincode,pay_id,status):
		self.contact=contact
		self.order=order
		self.ord_date=ord_date
		self.ord_address=ord_address
		self.status=status
		self.ord_time=ord_time
		self.pincode=pincode
		self.pay_id=pay_id

class PayCard(object):
	def __init__(self,contact,name,date,bill_addr,nick,ctype,number):
		self.contact=contact
		self.name=name
		self.date=date
		self.bill_addr=bill_addr
		self.nick=nick
		self.ctype=ctype
		self.number=number

class OrderList(object):
	def __init__(self,contact,ord_date,status,quant,price):
		self.contact=contact
		self.ord_date=ord_date
		self.status=status
		self.quant=quant
		self.price=price


class Cat(object):
	def __init__(self,pcat):
		self.pcat=pcat
    
