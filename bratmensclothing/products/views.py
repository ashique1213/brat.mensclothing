from django.shortcuts import render,redirect,get_object_or_404
from .models import Brand,Category,Product,Variant
from django.contrib import messages


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


def add_variants(request,product_id):
    product=get_object_or_404(Product,product_id=product_id)

    if request.method=='POST':
        variants_added = True
        image1=request.FILES.get('image1')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        image4=request.FILES.get('image4')
        size = request.POST.getlist('sizes[]')
        color = request.POST.getlist('colors[]')
        occation = request.POST.getlist('occasions[]')
        fit = request.POST.getlist('fit[]')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        variant = Variant(
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
            size=size,
            color=color,
            occation=occation,
            fit=fit,
            price=price,
            qty=quantity,
            status=True,  
            product=product,  
        )
        variant.save()
        # messages.success(request, 'Variant added successfully!')
        return redirect('view_variants', product_id=product_id)

    return render(request,'admin/add_variants.html', {'product': product})



def view_variants(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    variants = Variant.objects.filter(product=product)

    variants_added = variants.exists()

    return render(request, 'admin/variants.html', {'product': product, 'variants': variants,'variants_added': variants_added})
