from rest_framework import serializers

from pymongo import MongoClient
from .models import Product,Customer,Order,OrderList,Cat


client = MongoClient('localhost', 27017)
user_db= client.ssuk

class ProductSerializer(serializers.Serializer):
    shop_id = serializers.CharField(required=True, max_length=50)
    ptitle= serializers.CharField(required=True, max_length=100)
    pbrand= serializers.CharField(required=True, max_length=200)

    price= serializers.CharField(required=True)

    ppro= serializers.CharField(required=True)
    punit = serializers.CharField()
    plitres = serializers.CharField()
    pweight= serializers.CharField()
    package= serializers.CharField(max_length=50)
    pmin= serializers.CharField()
    pmax = serializers.CharField()
    pdisc = serializers.CharField()
    pexp= serializers.CharField()
    preddisc = serializers.CharField()
    pcat=serializers.CharField(max_length=50)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.shop_id = attrs.get('shop_id', instance.shop_id)
            instance.ptitle= attrs.get('ptitle', instance.ptitle)
            instance.pbrand = attrs.get('pbrand', instance.pbrand)
            instance.price = attrs.get('price', instance.price)
            instance.pmin= attrs.get('pmin', instance.pmin)
            instance.pmax= attrs.get('pmax', instance.pmax)
            instance.plitres= attrs.get('plitres', instance.plitres)
            instance.pweight= attrs.get('pweight', instance.pweight)
            instance.preddisc= attrs.get('preddisc', instance.preddisc)
            instance.pdisc= attrs.get('pdisc', instance.pdisc)
            instance.punit= attrs.get('punit', instance.punit)
            instance.pcat= attrs.get('pcat', instance.pcat)
            instance.package= attrs.get('package', instance.package)
            instance.ppro= attrs.get('ppro', instance.ppro)
            instance.pexp= attrs.get('pexp', instance.pexp)

            return instance

        return Product(attrs.get("shop_id"),attrs.get('ptitle'),attrs.get('pbrand'),attrs.get('punit'),attrs.get('pcat'),attrs.get('ppro'),attrs.get('plitres'),
				        attrs.get('package'),attrs.get('pweight'),attrs.get('pdisc'),attrs.get('pmin'),attrs.get('pmax'),attrs.get('preddisc'),attrs.get('pexp'),
				        attrs.get('price'))



class CustomerSerializer(serializers.Serializer):
    password=serializers.CharField()
    name=serializers.CharField()
    contact=serializers.CharField()
    name=serializers.CharField()
    address=serializers.CharField()
    orders=serializers.CharField()
    postcode=serializers.CharField()
    email=serializers.CharField()
    def create(self, attrs, instance=None):
        if instance:
            
            instance.password= attrs.get('password', instance.password)
            instance.address = attrs.get('address', instance.address)
            instance.contact = attrs.get('contact', instance.contact)
            instance.name= attrs.get('name', instance.name)
            instance.orders= attrs.get('orders', instance.orders)
            instance.postcode= attrs.get('postcode', instance.postcode)
            instance.email=attrs.get('email',instance.email)
            return instance

        return Customer(attrs.get('password'),attrs.get('address'),attrs.get('contact'),attrs.get('name'),attrs.get('orders'),attrs.get('postcode'),attrs.get('email'))


class OrderSerializer(serializers.Serializer):
    contact=serializers.CharField()
    order=serializers.CharField()
    ord_date=serializers.CharField()
    ord_address=serializers.CharField()
    status=serializers.CharField()
    ord_time=serializers.CharField()
    pincode=serializers.CharField()
    pay_id=serializers.CharField()
    
    
    def create(self, attrs, instance=None):
        if instance:
            instance.contact = attrs.get('contact', instance.contact)
            instance.ord_address = attrs.get('ord_address', instance.ord_address)
            instance.ord_date = attrs.get('ord_date', instance.contact)
            instance.order= attrs.get('order', instance.order)
            instance.status= attrs.get('status', instance.status)
            instance.ord_time=attrs.get('ord_time',instance.ord_time)
            instance.pincode=attrs.get('pincode',instance.pincode)
            instance.pay_id=attrs.get('pay_id',instance.pay_id)

            return instance

        return Order(attrs.get('contact'),attrs.get('order'),attrs.get('ord_date'),attrs.get('ord_address'),attrs.get('ord_time'),attrs.get('pincode'),attrs.get('pay_id'),attrs.get('status'))




class PaycardSerializer(serializers.Serializer):
    contact=serializers.CharField()
    name=serializers.CharField()
    date=serializers.CharField()
    bill_addr=serializers.CharField()
    nick=serializers.CharField()
    number=serializers.CharField()
    ctype=serializers.CharField()
    
    
    def create(self, attrs, instance=None):
        if instance:
            instance.contact = attrs.get('contact', instance.contact)
            instance.bill_addr = attrs.get('ord_address', instance.bill_addr)
            instance.date = attrs.get('ord_date', instance.date)
            instance.name= attrs.get('order', instance.name)
            instance.ctype= attrs.get('status', instance.ctype)
            instance.number=attrs.get('ord_time',instance.number)
            instance.nick=attrs.get('pincode',instance.nick)

            return instance

        return PayCard(attrs.get('contact'),attrs.get('name'),attrs.get('date'),attrs.get('bill_addr'),attrs.get('nick'),attrs.get('ctype'),attrs.get('number'))




class OrderListSerializer(serializers.Serializer):
    
    contact=serializers.CharField()
    ord_date=serializers.CharField()
    status=serializers.CharField()

    quant=serializers.CharField()
    price=serializers.CharField()
    
    def restore_object(self, attrs, instance=None):
        if instance:
            instance.ord_date = attrs.get('ord_date', instance.ord_date)
            instance.contact = attrs.get('contact', instance.contact)
            instance.status = attrs.get('status', instance.status)

            instance.quant = attrs.get('quant', instance.quant)
            instance.price = attrs.get('price', instance.price)

            return instance

        return OrderList(attrs.get('contact'),attrs.get('ord_date'),attrs.get('status'),attrs.get('quant'),attrs.get('price'))



class CatSerializer(serializers.Serializer):
    pcat=serializers.CharField()
    
    def create(self, attrs, instance=None):
        if instance:
            instance.pcat = attrs.get('pcat', instance.pcat)

            return instance

        return Cat(attrs.get('pcat'))
