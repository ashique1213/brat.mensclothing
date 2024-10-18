"""
URL configuration for bratmensclothing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('addbrands/',views.add_brands,name='add_brands'),
    path('viewbrands/', views.view_brands, name='view_brands'),
    path('addcategory/',views.add_category,name='add_category'),
    path('viewcategory/', views.view_category, name='view_category'),
    path('addproduct/',views.add_products,name='add_products'),
    path('', views.view_products, name='view_products'),
    path('addvariants/',views.add_variants,name='add_variants'),
    path('viewvariants/', views.view_variants, name='view_variants'),
    # path('', views.view, name=''),
    
]