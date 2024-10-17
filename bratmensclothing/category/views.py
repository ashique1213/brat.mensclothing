from django.shortcuts import render,redirect
from .models import Category

# Create your views here.


def add_category(request):
    if request.method=='POST':
        brand=request.POST.get('brandname')
        category=request.POST.get('category')
        unit=request.POST.get('categoryunit')

        val=Category.objects.create(brand_name=brand,category=category,category_unit=unit)
        print(val)
        return redirect('view_category')
    return render(request,'admin/category.html')

def view_category(request):
    categories=Category.objects.all()

    return render(request,'admin/category.html',{'categories':categories})