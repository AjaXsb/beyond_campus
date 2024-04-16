from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
def register(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if password1 != password2:
            # Handle password mismatch
            error_message = "Passwords do not match."
            return render(request, "signup.html", {"error_message": error_message})
        
        user = User.objects.create_user(username=username, email=email, password=password1, last_name=last_name, first_name=first_name)
        
        user.save()

        if user_type == "student":
            university = get_object_or_404(University, name=request.POST.get('university'))
            student = Student.objects.create(user=user, first_name= first_name, last_name=last_name, phone=phone, address=address, university=university)
            student.save()

        else:
            ssn = request.POST.get('ssn')
            landlord = Landlord.objects.create(user=user, first_name= first_name, last_name=last_name, phone=phone, address=address,ssn=ssn)
            landlord.save()

        return redirect(index)  # Redirect to the home page after successful registration

    universities = University.objects.order_by('name')

    return render(request, "signup.html", {"universities": universities})

def index(request):
    
    return render(request, "index.html")

def login_user(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            print("SUCCESFUL")
            return redirect(profile)

        else:
            print("unSUCCESFUL")
            return redirect(register)

    else:
        return render(request, "login.html")
    
def logout_user(request):

    logout(request)

    return redirect('login')

@login_required
def profile(request):

    try:
        # Try to fetch a Student object associated with the user
        user_info = Student.objects.get(user=request.user)
        user_type = 'student'

    except Student.DoesNotExist:
        try:

            # Try to fetch a Landlord object associated with the user
            user_info = Landlord.objects.get(user=request.user)
            user_type = 'landlord'

        except Landlord.DoesNotExist:
            # Handle the case where the user does not have a Student or Landlord object
            user_info = None
            user_type = None

    return render(request, "profile.html", {"user_info": user_info, "user_type": user_type})