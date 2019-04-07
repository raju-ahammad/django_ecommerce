from django.shortcuts import render
from django.views.generic import ListView, DetailView
from products.models import Product

class SearchListView(ListView):
    template_name  = 'search/list.html'
    context_object_name = 'product'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchListView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.active()
