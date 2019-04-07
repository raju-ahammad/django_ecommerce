from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed
from products.models import Product
from decimal import Decimal
# Create your models here.
User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user_obj
        return self.model.objects.create(user=user_obj)


    def new_cart(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = Cart.objects.filter(id=cart_id)
        print(cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
            print(cart_id)

        return cart_obj, new_obj






class Cart(models.Model):
    PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
    user       = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product    = models.ManyToManyField(Product, blank=True)
    total      = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    subtotal   = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    update     = models.DateTimeField(auto_now_add=True)
    timestamp  = models.DateTimeField(auto_now_add=True)
    quantity   = models.IntegerField(choices=PRODUCT_QUANTITY_CHOICES, default=0)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, action, instance, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.product.all()
        subtotal = 0
        #quantity = instance.quantity
        for product in products:
            subtotal += product.price
        subtotal = subtotal

        instance.subtotal = subtotal
        vat  = Decimal(100)*Decimal(0.05)
        total = Decimal(subtotal) + Decimal(vat)
        instance.total = total
        instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.product.through)


# def pre_save_cart_receiver(sender, instance, *args, **kwargs):
#      quantity = instance.quantity
#      if instance.quantity > 0:
#          instance.subtotal = instance.subtotal*quantity
#      else:
#          instance.subtotal = subtotal
#
# pre_save.connect(pre_save_cart_receiver, sender=Cart)
