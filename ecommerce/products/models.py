from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from django.db.models import Q
from django.urls import reverse


# Create your models here.
class ProductQueryset(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True, active=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        looksup = Q(title__contains=query) | Q(description__contains=query) | Q(price__contains=query) | Q(tag__title__contains=query)
        return self.filter(looksup).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()


    def features(self):
        return self.get_queryset().featured()


    def active(self):
        return self.get_queryset().active()


    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)  #Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title         = models.CharField(max_length=120)
    slug          = models.SlugField(blank=True, null=True, unique=True)
    description   = models.TextField()
    price         = models.DecimalField(max_digits=20, decimal_places=2, default=99.99)
    image         = models.ImageField(default='default.png', blank = True, null=True)
    featured      = models.BooleanField(default=False)
    active        = models.BooleanField(default=True)

    class Meta():
        ordering = ('-title',)



    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('slug_detail', kwargs={'slug': self.slug})


    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
