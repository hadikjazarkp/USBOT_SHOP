from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import Http404
from .email import *
from django.urls import reverse
from Store.models import UserProfile
from Store.forms import CustomUserForm
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

from django.core.cache import cache
import hashlib
import random
from django.views import View
from Store.forms import CustomUserForm







class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.success(request, "Already Registered! Login to Continue")
            return redirect('home')
        else:
            form = CustomUserForm()
            context = {'form': form}
            return render(request, "store/auth/register.html", context)

    def post(self, request):
        form = CustomUserForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Check if a file was provided
            if 'profile_image' in request.FILES:
                profile_image = form.cleaned_data['profile_image']
            else:
                profile_image = None  # Set to None if no file provided

            # Send success message and OTP email
            messages.success(request, "Registered Successfully! Login to Continue")
            otp = str(random.randint(100000, 999999))
            send_otp_email(form.cleaned_data['email'], form.cleaned_data['username'], otp)
            
            # Generate cache key and store registration data
            key = hashlib.sha256(form.cleaned_data['email'].encode()).hexdigest()
            cache.set(
                key,
                {"email": form.cleaned_data['email'], "username": form.cleaned_data['username'],
                 "password": form.cleaned_data['password1'], "otp": otp},
                timeout=600
            )

            # Redirect to OTP verification
            return redirect("otp", key=key)
        else:
            # Add an error message
            messages.error(request, "Please correct the errors below.")
            return render(request, "store/auth/register.html", {'form': form})



class VerifyOtpView(View):
    def get(self, request, key):
        # Render the OTP verification form
        return render(request, "store/auth/otp.html", {"key": key})

    def post(self, request, key):
        receivedotp = request.POST.get("otp")

        signup_data = cache.get(key)
        print(signup_data)
        if not signup_data:
            messages.warning(request, "OTP expired or invalid")
            return redirect("otp", key=key)
        otp = signup_data.get("otp")
        username = signup_data.get("username")
        email = signup_data.get("email")
        password = signup_data.get("password")
        
        print(otp)
        if receivedotp != otp:
            messages.warning(request, "OTP mismatch")
            return redirect("otp", key=key)

        user = UserProfile.objects.create_user(
            username=username, email=email, password=password, 
        )
        user.save()
        cache.delete(key)
        return redirect("loginpage")



class ResendOTP(View):
    def get(self, request, key):
        signup_data = cache.get(key)
        if signup_data:
            email = signup_data.get("email")
            username = signup_data.get("username")
            otp = str(random.randint(100000, 999999))
            print(otp)
            send_otp_email(email, username, otp)
            signup_data["otp"] = otp
            existing_timeout = signup_data.get("timeout", None)
            cache.set(key, signup_data, timeout=existing_timeout)
            return redirect("otp", key=key)
        return redirect("register")


class SignIn(View):
    def get(self, request):

        if request.user.is_authenticated:
            messages.warning(request, "YOU are already logged in")
            return redirect('home')
        else: 
            return render(request, "store/auth/login.html")
        
    def post(self, request):

        # if request.method == 'POST':
        email = request.POST.get('email')
        passwd = request.POST.get('password')
    
        user = authenticate(request, email=email, password=passwd)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("home")
            else:
                messages.error(request, "Account is Banned")
                return redirect("loginpage")
            
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("loginpage")
        
        
        
class ForgotPassword(View):
    def get(self, request):
        return render(request, "store/auth/password_forgot_form.html")
    
    def post(self, request):
        email = request.POST.get("email")
        try:
            user = UserProfile.objects.get(email=email)
        except:
            messages.warning(request, "You are not registerd, please sign up")
            return redirect("register")
        encrypt_id = urlsafe_base64_encode(str(user.email).encode())
        reset_link = f"{request.scheme}://{request.get_host()}{reverse('reset', args=[encrypt_id])}"
        print(reset_link)
        cache_key = f"reset_link_{encrypt_id}"
        cache.set(cache_key, {"reset_link": reset_link}, timeout=200)
        reset_password_email(email, reset_link)
        messages.success(request, "Password reset link sent to your email.")
        return redirect("loginpage")

class UserResetPassword(View):
    def get(self, request, encrypt_id):
        cache_key = f"reset_link_{encrypt_id}"
        cache_data = cache.get(cache_key)
        if not cache_data:
            raise Http404("Reset link has expired") 
        reset_id = cache_data.get("reset_link")
        return render(request, "store/auth/password_reset.html",{"reset": reset_id})
    
    def post(self, request, encrypt_id ):
        cache_key = f"reset_link_{encrypt_id}"
        email = str(urlsafe_base64_decode(encrypt_id), "utf-8")
        user = UserProfile.objects.get(email=email)
        new_password = request.POST.get("pass1") 
        print(new_password)
        user.set_password(new_password)
        user.save()
        cache.delete(cache_key) 
        messages.success(
            request,
            "Password reset successful. You can now log in with your new password.",
        ) 
        return redirect("loginpage")
        
class Logoutpage(View):
    def get (self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "Logged out Successfully ")
            return redirect("home")
    
           
    
    
    