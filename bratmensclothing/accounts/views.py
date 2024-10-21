from django.shortcuts import render,redirect
from . models import Users
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import re
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from django.urls import reverse



def signup_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        errors = {}
        
        if any(char.isdigit() or char.isspace() for char in username):
            errors['username_error'] = 'Username should not contain numbers or spaces'

        if Users.objects.filter(username=username).exists():
            errors['username_error'] = 'Username already exists'

        if Users.objects.filter(email=email).exists():
            errors['email_error'] = 'Email is already exists'

        if pass1 != pass2:
            errors['password_error'] = 'Passwords do not match'

        # if len(pass1) < 8:
        #     errors['password_error'] = 'Password must be at least 8 characters long'
        # if not re.search(r'[A-Z]', pass1):
        #     errors['password_error'] = 'Password must contain at least one uppercase letter'
        # if not re.search(r'[a-z]', pass1):
        #     errors['password_error'] = 'Password must contain at least one lowercase letter'
        # if not re.search(r'[0-9]', pass1):
        #     errors['password_error'] = 'Password must contain at least one number'
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pass1):
        #     errors['password_error'] = 'Password must contain at least one special character'
        

        if errors:
            # Return JSON response with errors
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)
        
        else:
            hashed_password = make_password(pass1)
            new_user=Users.objects.create(username=username,phone_number=phone,email=email,password=hashed_password)
            new_user.save()
            return JsonResponse({'status': 'success', 'message': 'User created successfully'}, status=200)
    return render(request, 'user/signup.html')



def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Username: {email}")
        print(f"Password: {password}")

        try:
            user = Users.objects.get(email=email)

            if user.isBlocked:
                print('User is blocked.')
                return JsonResponse({'status': 'error', 'errors': {'account': 'Your account is blocked.'}}, status=403)
            
            if check_password(password, user.password):
                print('User authenticated successfully.')

                redirect_url = reverse('home_user')
                return JsonResponse({'status': 'success', 'redirect_url': redirect_url}, status=200)
            else:
                print('Invalid password')
                return JsonResponse({'status': 'error', 'errors': {'password': 'Invalid password'}}, status=400)
       
        except Users.DoesNotExist:
            print('User does not exist')
            return JsonResponse({'status': 'error', 'errors': {'email': 'User does not exist'}}, status=400)

    return render(request, 'user/login.html')


def home_user(request):
    
    return render(request,'user/home.html')



