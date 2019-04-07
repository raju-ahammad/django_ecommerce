from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from .models import Cart
from products.models import Product
from orders.models import Order
from auths.forms import LoginForm
from django.contrib.auth.decorators import login_required
from billing.models import BillingProfile
#class CartListView(TemplateView):
    #template_name  = 'carts/home.html'


def cart_view(request):
    cart_obj, new_obj = Cart.objects.new_cart(request)
    return render(request, 'carts/home.html', {'cart':cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show massage to user product is gone")
            return redirect('cart')
        cart_obj, new_obj = Cart.objects.new_cart(request)
        if product_obj in cart_obj.product.all():
            cart_obj.product.remove(product_obj)
        else:
            cart_obj.product.add(product_obj)
        request.session['cart_item'] = cart_obj.product.count()
    return redirect('cart')



def cheakout(request):
    cart_obj, cart_created = Cart.objects.new_cart(request)
    order_obj = None
    if cart_created or cart_obj.product.count() == 0:
        return redirect('cart')
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    if billing_profile is not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            # old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            # if old_order_qs.exists():
            #     old_order_qs.update(active=False)
            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)



    context = {
          'object' : order_obj,
          'billing_profile' : billing_profile,
          'login_form' : login_form
    }

    return render(request, "carts/cheakout.html", context)
