import os
import requests
import json
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators  import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.db import connection
from opentelemetry import trace as OpenTelemetry

from products.models import Product
from .models import Order, OrderItem
from .models import RefundForm

# OTEL Manual Instrumentation
class DatabaseLogger:
    '''Class to help wrap db calls for OpenTelemetry'''
    def __call__(self, execute, sql, params, many, context):
        tracer = OpenTelemetry.get_tracer(__name__)
        with tracer.start_as_current_span("SQLite3 db call"):
            current_span = OpenTelemetry.get_current_span()
            current_span.set_attribute("db_query", sql)
            current_span.set_attribute("db_connection", str(context['connection']))
            current_span.set_attribute("db_cursor", str(context['cursor']))
            return execute(sql, params, many, context)

class RefundView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'carts/refund.html'
    form_class = RefundForm
    success_url = reverse_lazy('refund')
    success_message = "The request for a refund has been successfully sent"

    def form_valid(self, form):
        try:
            order = Order.objects.get(order_id=form.cleaned_data['order_id'])
        except Order.DoesNotExist:
            messages.warning(self.request, "Provided order id does not exists")
            return redirect('refund')
        order.refund_requested = True
        order.save()
        form.instance.user = self.request.user
        form.instance.order = order
        return super().form_valid(form)

# OTEL Manual Instrumentation
class OrdersListView(LoginRequiredMixin, ListView):
    context_object_name = 'orders'

    def get_queryset(self):
        dbl = DatabaseLogger()
        with connection.execute_wrapper(dbl):
            return self.request.user.order_set.filter(ordered=True)

# OTEL Manual Instrumentation
class CartDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'order'
    template_name = 'carts/cart.html'

    def get_object(self, queryset=None):
        dbl = DatabaseLogger()
        with connection.execute_wrapper(dbl):
            return self.request.user.order_set.filter(ordered=False).first()

# OTEL Manual Instrumentation
class AddToCartAjax(View):
    def post(self, request, product_id, *args, **kwargs):
        tracer = OpenTelemetry.get_tracer(__name__)
        with tracer.start_as_current_span("AJAX Add to Cart"):
            if not self.request.user.is_authenticated:
                return JsonResponse({
                    'error': 'In order to add item to cart please create an account'
                }, status=401)
            if self.request.is_ajax:
                product = get_object_or_404(Product, pk=product_id)
                order, _ = Order.objects.get_or_create(user=self.request.user, ordered=False)
                if order.items.filter(item__pk=product_id).exists():
                    order_item = order.items.get(item__pk=product_id)
                    order_item.quantity += 1
                    order_item.save()
                else:
                    order_item = OrderItem.objects.create(user=self.request.user, item=product)
                    order.items.add(order_item)
                # Pass release-version details in the header if environment variable is set
                if "DT_RELEASE_VERSION" in os.environ:
                    return JsonResponse({
                    'msg': "Product has been successfully added to cart",
                    'quantity': order_item.quantity,
                    'total_items': order.get_total_quantity(),
                    })
                else:
                    return JsonResponse({
                    'msg': "Product has been successfully added to cart",
                    'quantity': order_item.quantity,
                    'total_items': order.get_total_quantity()
                    })


@login_required
def increase_product_in_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order, _ = Order.objects.get_or_create(user=request.user, ordered=False)
    if order.items.filter(item__pk=product_id).exists():
        order_item = order.items.get(item__pk=product_id)
        order_item.quantity += 1
        order_item.save()
    else:
        order.items.create(user=request.user, item=product)
    messages.success(request, 'Product has been added to cart.')
    return redirect('carts:show-cart')


@login_required
def decrease_product_in_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order:
        order_item = order.items.filter(user=request.user, item=product).first()
        if order_item:
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity <= 0:
                order.items.remove(order_item)
            messages.success(request, 'Product has been removed from cart.')
        else:
            messages.warning(request, 'This item is not in your cart.')
    else:
        messages.warning(request, 'Cart does not exists. Add some products to cart.')
        return redirect('products:home-page')
    return redirect('carts:show-cart')


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order:
        order_item = order.items.filter(user=request.user, item=product).first()
        if order_item:
            order.items.remove(order_item)
            messages.success(request, 'Product has been removed from cart.')
        else:
            messages.warning(request, 'This item is not in your cart.')
    else:
        messages.warning(request, 'Cart does not exists. First add products to cart.')
        return redirect('products:home-page')
    return redirect('carts:show-cart')
