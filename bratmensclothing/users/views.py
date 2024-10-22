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
    return redirect('userss:view_user')


def unblock_user(request,user_id):
    users=get_object_or_404(Users,user_id=user_id)
    users.isBlocked=False
    users.save()
    messages.success(request,'User Blocked Succesfully')
    return redirect('userss:view_user')


