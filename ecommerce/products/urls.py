from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.ProductListView.as_view(), name= 'home'),
    path('product/', views.ProductListView.as_view(), name= 'product'),
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name= 'detail'),
    path('fetured/', views.ProductFeturedListView.as_view(), name= 'fetured'),
    path('fetured_detail/<int:pk>', views.ProductFeturedDetailView.as_view(), name= 'fet_detail'),
    path('detail/<slug:slug>', views.SlugDetailView.as_view(), name= 'slug_detail'),
]

urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
