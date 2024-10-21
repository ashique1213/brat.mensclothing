from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Users
from django.contrib import messages


def view_user(request):
    users=Users.objects.all()

    return render(request,'admin/users.html',{'users':users})


def block_user(request,user_id):
    users=get_object_or_404(Users,user_id=user_id)
    users.isBlocked=True
    users.save()
    messages.success(request,'User Blocked Succesfully')
    return redirect('view_user')


def unblock_user(request,user_id):
    users=get_object_or_404(Users,user_id=user_id)
    users.isBlocked=False
    users.save()
    messages.success(request,'User Blocked Succesfully')
    return redirect('view_user')



# def soft_delete_brand(request,brand_id):
#     brand= get_object_or_404(Brand,brand_id=brand_id)
#     brand.is_deleted=True
#     brand.save()

#     messages.success(request, 'Brand successfully soft deleted!')
#     return redirect('view_brands')

# def restore_brand(request,brand_id):
#     brand= get_object_or_404(Brand,brand_id=brand_id)
#     brand.is_deleted=False
#     brand.save()
#     messages.success(request, 'Brand successfully restored!')
#     return redirect('view_brands')