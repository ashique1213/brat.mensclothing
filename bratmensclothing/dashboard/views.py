from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
# from accounts.models  import 




def admin_dashboard(request):
    
    return render(request, 'admin/dashboard.html')