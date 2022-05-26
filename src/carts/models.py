import requests
import json
import os
from django.db import models
from django.conf import settings
from django import forms

from products.models import Product
from checkout.models import ShippingAddress
from checkout.models import Payment
from opentelemetry import trace as OpenTelemetry


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item.name}: {self.quantity}'

    def get_total(self):
        return round(self.item.price * self.quantity, 2)


class Order(models.Model):
    order_id = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    promo_code_applied = models.BooleanField(default=False)
    promo_code_discount = models.FloatField(default=0)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.get_all_items()}'

    def get_all_items(self):
        return [item for item in self.items.all()]

    def get_total_amount(self):
        total = sum(item.get_total() for item in self.items.all())
        return total - self.promo_code_discount

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    # Otel Manuel Instrumentation
    def convert_currency(self):
        tracer = OpenTelemetry.get_tracer(__name__)
        with tracer.start_as_current_span("Making Request to Currency Service") as span:
            # Grabs traceid and spanid for context propagation
            
            context = span.get_span_context()
            trace_id = OpenTelemetry.format_trace_id(context.trace_id)
            span_id = OpenTelemetry.format_span_id(context.span_id)
            trace_parent = "00-" + trace_id + "-" + span_id + "-" + "01"

    #############################################################################################
    #############################################################################################            
            headers = {
                'Content-Type': 'application/json',
                'traceparent': trace_parent
            }
    #############################################################################################
    ####################### Use top section for context propagation #############################
    #############################################################################################      
    #        headers = {
    #            'Content-Type': 'application/json'
    #        }        
    #############################################################################################
    #############################################################################################
            payload = {
                "from": {
                    "currency_code": "USD",
                    "units": self.get_total_amount(),
                    "nanos": self.get_total_amount() % 1.0
                },
                "to": "EUR"
            }
            url = os.environ.get("CURRENCYSERVICE_URL")
            try:
                r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=1)
            except:
                print("Request to Currency Converter Failed")
                return -1


            response = r.json()
            units = response['units']
            nanos = round(response['nanos'], 2)
            totalString = f'{units}.{nanos}'
            total = float(totalString)
            return total


class Refund(models.Model):
    reason = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    granted = models.BooleanField(default=False)

    def __str__(self):
        return f'Refund for order {self.order.order_id}'


class RefundForm(forms.ModelForm):
    order_id = forms.CharField()

    class Meta:
        model = Refund
        fields = ['order_id', 'reason']