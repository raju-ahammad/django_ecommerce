from django.shortcuts import render, Http404,  get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product
from cart.models import Cart

class ProductFeturedListView(ListView):
    model    = Product
    template_name = 'product/featured_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductFeturedListView, self).get_context_data(*args, **kwargs)
        context['product'] = Product.objects.all().featured()
        return context

    def get_queryset(self):
        request = self.request
        qs = Product.objects.all().featured()
        return qs



class ProductFeturedDetailView(DetailView):
    model    = Product
    #queryset = Product.objects.all()
    template_name = 'product/fetured_detail.html'

    def get_queryset(self):
        request = self.request
        qs = Product.objects.featured()
        return qs




class ProductListView(ListView):
    model    = Product
    template_name = 'product/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['product'] = Product.objects.all()
        return context




class ProductDetailView(DetailView):
    model    = Product
    template_name = 'product/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404('Product doesnot exist')
        return instance



class SlugDetailView(DetailView):
    model    = Product
    template_name = 'product/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SlugDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_cart(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Product, slug=slug, active=True)
        return instance
