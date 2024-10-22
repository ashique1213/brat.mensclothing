from django.shortcuts import render,redirect
from . models import Users
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import re
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from django.urls import reverse
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta



# def generate_otp():
#     return random.randint(100000, 999999)

# def signup_user(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         phone=request.POST.get('phone')
#         email=request.POST.get('email')
#         pass1=request.POST.get('password1')
#         pass2=request.POST.get('password2')
        
#         # errors = {}
        
#         # if any(char.isdigit() or char.isspace() for char in username):
#         #     errors['username_error'] = 'Username should not contain numbers or spaces'

#         # if Users.objects.filter(username=username).exists():
#         #     errors['username_error'] = 'Username already exists'

#         # if Users.objects.filter(email=email).exists():
#         #     errors['email_error'] = 'Email is already exists'

#         # if pass1 != pass2:
#         #     errors['password_error'] = 'Passwords do not match'

#         # if len(pass1) < 8:
#         #     errors['password_error'] = 'Password must be at least 8 characters long'
#         # if not re.search(r'[A-Z]', pass1):
#         #     errors['password_error'] = 'Password must contain at least one uppercase letter'
#         # if not re.search(r'[a-z]', pass1):
#         #     errors['password_error'] = 'Password must contain at least one lowercase letter'
#         # if not re.search(r'[0-9]', pass1):
#         #     errors['password_error'] = 'Password must contain at least one number'
#         # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pass1):
#         #     errors['password_error'] = 'Password must contain at least one special character'
        
#         # if errors:
#         #     # Return JSON response with errors
#         #     return JsonResponse({'status': 'error', 'errors': errors}, status=400)
        
#         # else:
#         #     hashed_password = make_password(pass1)
#         #     new_user=Users.objects.create(username=username,phone_number=phone,email=email,password=hashed_password)
#         #     new_user.save()
#         #     return JsonResponse({'status': 'success', 'message': 'User created successfully'}, status=200)


#         otp = generate_otp()
#         otp_expiry = timezone.now() + timedelta(minutes=3)
        
#         # Store OTP and expiry time in the session
#         request.session['otp'] = otp
#         request.session['otp_expiry'] = otp_expiry.isoformat()
#         request.session['email'] = email
#         request.session['username'] = username
#         request.session['phone'] = phone
#         request.session['password'] = pass1
        
#         # Send OTP to email
#         send_mail(
#             'Your OTP Code',
#             f'Your OTP code is {otp}',
#             'your_email@example.com',
#             [email],
#             fail_silently=False,
#         )
#         return redirect('accounts:otp_verify')
    
#     return render(request, 'user/signup.html')

# def otp_verify(request):

#     return render(request,'user/otp.html')


# Generate a 6-digit OTP
def generate_otp():
    return random.randint(100000, 999999)

# Signup View
def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Ensure passwords match
        if pass1 == pass2:
            # Generate and store OTP in session
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['username'] = username
            request.session['phone'] = phone
            request.session['password'] = pass1  # Store password for later user creation

            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'your_email@example.com',  # Replace with your email
                [email],
                fail_silently=False,
            )

            # Redirect to OTP verification page
            return redirect('accounts:otp_verify')

        else:
            # If passwords do not match
            return render(request, 'user/signup.html', {'error': 'Passwords do not match.'})

    return render(request, 'user/signup.html')

# OTP Verification View
def otp_verify(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')  # Get the OTP entered by the user
        stored_otp = request.session.get('otp')  # Get the OTP stored in the session

        # Debugging session values
        print(f"Entered OTP: {entered_otp}, Stored OTP: {stored_otp}")

        if entered_otp == str(stored_otp):  # If OTP is correct
            # Create user with session data
            user = Users.objects.create_user(
                email=request.session['email'],
                username=request.session['username'],
                phone=request.session['phone'],
                password=request.session['password'],  # Properly pass the password field
            )
            user.save()

            # Clear session data
            request.session.flush()

            # Redirect to home page with success message
            messages.success(request, "Account created successfully!")
            return redirect('accounts:home_user')
        else:
            # If OTP is incorrect
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('accounts:otp_verify')

    return render(request, 'user/otp.html')

# Resend OTP View
def resend_otp(request):
    email = request.session.get('email')  # Get the email stored in session

    if email:
        # Generate a new OTP
        otp = generate_otp()
        request.session['otp'] = otp  # Update the OTP in session

        # Resend the OTP via email
        send_mail(
            'Your New OTP Code',
            f'Your new OTP code is {otp}',
            'your_email@example.com',  # Replace with your email
            [email],
            fail_silently=False,
        )

        messages.success(request, 'A new OTP has been sent to your email.')
        return redirect('accounts:otp_verify')
    else:
        messages.error(request, 'An error occurred. Please try signing up again.')
        return redirect('accounts:signup_user')










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


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f'Email: {email}, Password: {password}')  

        try:
            admin = User.objects.get(email=email)
            print(f'User found: {admin.username}')  
        except User.DoesNotExist:
            admin = None
            print('User not found')  
        
        if admin is not None:
            admin = authenticate(request, username=admin.username, password=password)

            if admin is not None and admin.is_superuser:
                login(request, admin)
                print('logged in')
                # return render(request,'admin/dashboard.html')
                return redirect('admin_dashboard')
        
        error_message = "Invalid credentials or not a superuser."
        print('Authentication failed')  
        return render(request, 'admin/admin_login.html', {'error_message': error_message})

    return render(request, 'admin/admin_login.html')


def admin_logout(request):
    logout(request)
    return redirect('accounts:admin_login')


