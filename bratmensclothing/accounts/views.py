from django.shortcuts import render

# Create your views here.
def user_home(request):
    return render(request,'productdetails.html')