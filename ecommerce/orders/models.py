from django.db import models
from cart.models import Cart
from ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
import math
from billing.models import BillingProfile


ORDER_STATUS_CHOICES = (
       ('created', 'Created'),
       ('paid', 'Paid'),
       ('shipped', 'Shipped'),
       ('refunded', 'Refunded'),
)


class Order(models.Model):
    billing_profile  = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    order_id         = models.CharField(max_length=120, blank=True)
    cart             = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status           = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total   = models.DecimalField(max_digits=100, decimal_places=2, default=5.99)
    total            = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    active           = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formated_total = format(new_total, '.2f')
        self.total = formated_total
        self.save()
        return formated_total




def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.updat(active=False)   


pre_save.connect(pre_save_create_order_id, sender=Order)



def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id    = cart_obj.id
        qs = Order.objects.filter(cart_id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    print('running....')
    if created:
        print('updating .... first')
        instance.update_total()

post_save.connect(post_save_order, sender=Order)
