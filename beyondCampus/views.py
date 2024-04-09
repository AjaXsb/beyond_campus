from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404


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
        
        user = User.objects.create(username=username, email=email, password=password1, last_name=last_name, first_name=first_name)
        
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