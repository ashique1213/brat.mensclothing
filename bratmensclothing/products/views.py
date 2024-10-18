from django.shortcuts import render,redirect
from .models import Brand,Category,Product


def add_brands(request):
    if request.method=='POST':
        brand=request.POST.get('brandname')

        value=Brand.objects.create(brandname=brand)
        print(value)
        return redirect('view_brands')
    return render(request,'admin/add_brand.html')

def view_brands(request):
    Brands=Brand.objects.all()

    return render(request,'admin/brand.html',{'brand':Brands})



def add_category(request):
    if request.method=='POST':
        category=request.POST.get('category')
        categorytype=request.POST.get('categorytype')

        value=Category.objects.create(category=category,category_type=categorytype)
        print(value)
        return redirect('view_category')
    return render(request,'admin/add_category.html')

def view_category(request):
    category=Category.objects.all()

    return render(request,'admin/category.html',{'category':category})


def add_products(request):
    if request.method == 'POST':
        productname = request.POST.get('productname')
        description = request.POST.get('description')
        brand = request.POST.get('brandname')
        category_ids = request.POST.getlist('category')  

        try:
            brand = Brand.objects.get(brandname=brand)
        except Brand.DoesNotExist:
            brand = None  

        product = Product.objects.create(
            product_name=productname,
            description=description,
            brand=brand
        ) 
        product.category.set(category_ids)   
        return redirect('view_products')  
    
    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'admin/add_product.html', {'categories': categories,'brands': brands})

  

def view_products(request):
    products=Product.objects.all()

    return render(request,'admin/product.html',{'products':products})


def add_variants(request):

    return render(request,'admin/add_variants.html')



def view_variants(request):

    return render(request,'admin/variants.html')


def view(request):
    return render(request,'user/adminproduct.html')