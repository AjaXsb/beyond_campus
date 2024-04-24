from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse
from django.db.models import Avg
from django.contrib import messages

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
    listings = Listing.objects.all()

    ## Calculate average ratings for each listing
    #for listing in listings:
    #    property_obj = Property.objects.get(listing=listing)
    #    avg_rating = Review.objects.filter(property=property_obj).aggregate(Avg('rating'))['rating__avg']
    #    listing.avg_rating = avg_rating if avg_rating else "No ratings yet"

    # Prepare data to pass to the template
    data = {
        'listings': listings
    }

    # Render the template with the data
    return render(request, 'index.html', data)
    
    
def login_user(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        print(user)
        
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

    properties = None  # Define properties variable outside the try-except block

    try:
        # Try to fetch a Student object associated with the user
        user_info = Student.objects.get(user=request.user)
        user_type = 'student'
    
        return render(request, "student_dashboard.html", {"user_info": user_info, "user_type": user_type, "properties": properties})
    
    except Student.DoesNotExist:
        try:
            # Try to fetch a Landlord object associated with the user
            user_info = Landlord.objects.get(user=request.user)
            user_type = 'landlord'
            properties = Property.objects.filter(landlordown__landlord=user_info)

            return render(request, "landlord_dashboard.html", {"user_info": user_info, "user_type": user_type, "properties": properties})

        except Landlord.DoesNotExist:
            # Handle the case where the user does not have a Student or Landlord object
            user_info = None
            user_type = None
            
            return redirect(index)
    

def report_issue(request, property_id):
    property = get_object_or_404(Property, pk=property_id)

    if request.method == 'POST':
        issue_description = request.POST.get('issue')
        if issue_description:
            # Assume 'student' relation on the user and 'Report' has a 'property' field
            Report.objects.create(property=property, student=request.user.student, description=issue_description)
            messages.success(request, "Your report has been submitted successfully!")
            return redirect('report_issue', property_id=property_id)

    context = {
        'property': property,
    }
    return render(request, 'report.html', context)


def property_reviews(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    reviews = Review.objects.filter(property=property)

    if request.method == 'POST':
        review_text = request.POST.get('review')
        if review_text:
            # Create a new Review object assuming there is a 'student' relation on the user
            Review.objects.create(property=property, student=request.user.student, comment=review_text)
            messages.success(request, "Your review has been submitted!")
            return redirect('property_reviews', property_id=property_id)

    context = {
        'property': property,
        'reviews': reviews
    }
    return render(request, 'review.html', context)


@login_required
def add_to_favourites(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    student = get_object_or_404(Student, pk=request.user.student.id)
    if request.method == 'POST':
        Fav.objects.get_or_create(student=student, property=property)
        messages.success(request, f"{property.name} has been added to your favourites!")
        return redirect('favourite', property_id=property_id)  # Redirect to the same page or to the favourites list

    return render(request, 'favourite.html', {'property': property})

def show_favourites(request,student_id):
    favourites = Fav.objects.filter(user=request.student)  # Assuming you filter by logged-in user
   # student = get_object_or_404(student, student_id)
    return render(request, 'myfavourite.html', {'favourites': favourites})

@login_required
def my_favourites(request):
    student = get_object_or_404(Student, pk=request.user.student.id)
    favourites = Fav.objects.filter(student=student).select_related('property')
    return render(request, 'myfavourite.html', {'favourites': favourites})

def student_dashboard(request):
    # Assuming each user is linked to a student and each student is linked to exactly one property
    student = get_object_or_404(Student, user=request.user)
    property = get_object_or_404(Property, student=student)

    context = {
        'property': property,
    }
    return render(request, 'student_dashboard.html', context)

def myhouse_dashboard(request):
    current_occupy = Occupy.objects.filter(student__user=request.user).first()
    if not current_occupy:
        messages.error(request, "You do not have a current residence.")
        return redirect('student_dashboard.html')
    request.session['property_id'] = current_occupy.property.id
    return render(request, 'Myhouse.html', {'property': current_occupy.property})

def request_maintenance(request):
    student = get_object_or_404(Student, pk=request.user.student.id)
    property_id = request.session.get('property_id')
    if not property_id:
        messages.error(request, "Property not specified.")
        return redirect('myhouse_dashboard.html')
    maintenance_requests = RequestMaintenance.objects.filter(property__id=property_id, student=student)
    return render(request, 'Request_Maintenance.html', {'maintenance_requests': maintenance_requests })

def insurance_coverage(request):
    property_id = request.session.get('property_id')
    if not property_id:
        messages.error(request, "Property not specified.")
        return redirect('myhouse_dashboard.html')
    coverage = CoveredBy.objects.filter(property__id=property_id)
    return render(request, 'Insurance.html', {'coverage': coverage})

def utility_provide(request):
    property_id = request.session.get('property_id')
    if not property_id:
        messages.error(request, "Property not specified.")
        return redirect('myhouse_dashboard.html')
    utility_providers = UtilityProvide.objects.filter(property__id=property_id).select_related('provider')
    return render(request, 'UtilityProvider.html', {'utility_providers': utility_providers})


@login_required
def show_student_applications(request):
    try:
        student = request.user.student  # Assuming the student is related to the User model

        # Get all applications associated with the student
        applications = Apply.objects.filter(student=student)

        # Retrieve the status for each application
        for application in applications:
            waitlist = Waitlist.objects.filter(student=student, listing=application.listing).first()
            if waitlist:
                application.status = waitlist.status
            else:
                application.status = "Unknown"

        # Prepare data to pass to the template
        data = {
            'applications': applications
        }

        return render(request, 'show_student_applications.html', data)
    
    except Student.DoesNotExist:
        return redirect(index)

@login_required
def show_landlord_applications(request):
    try:
        landlord = Landlord.objects.get(user=request.user)
            
        # Get all listings associated with the landlord
        listings = Listing.objects.filter(landlord=landlord)

        # Fetch applications for each listing
        applications = []
        for listing in listings:
            listing_applications = Apply.objects.filter(listing=listing)
            for application in listing_applications:
                applications.append(application)

        # Prepare data to pass to the template
        data = {
            'applications': applications
        }

        return render(request, 'show_landlord_applications.html', data)

    except Landlord.DoesNotExist:
        return redirect(index)

    
    
@login_required
def create_listing(request):
    if request.method == 'POST':
        # Extract data from the request.POST dictionary
        title = request.POST.get('title')
        rent = request.POST.get('rent')
        room = request.POST.get('room')
        amenities = request.POST.get('amenities')
        property_id = request.POST.get('property')

        # Get the Property object based on the selected property_id
        property_obj = Property.objects.get(id=property_id)

        # Create the listing object
        listing = Listing.objects.create(
            title=title,
            rent=rent,
            room=room,
            amenities=amenities,
            landlord=request.user.landlord,
        )
        
        # Redirect to the profile page after creating the listing
        return redirect('profile')

    else:
        # Fetch all properties owned by the current user (landlord)
        properties_owned = Property.objects.filter(landlord=request.user.landlord)
    
        return render(request, 'profile.html', {'properties_owned': properties_owned})

import random

@login_required
def apply_to_listing(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        preferences = request.POST.get('preferences')
        additional_info = request.POST.get('additional_info')

        min_num = 100000  # Minimum application number
        max_num = 999999  # Maximum application number
        application_num = random.randint(min_num, max_num)


        
        # Create the application
        application = Apply.objects.create(
            student=request.user.student,
            listing=listing,
            application_num=application_num,
            preferences=preferences,
            additional_info=additional_info
        )

        # Create a waitlist entry
        waitlist_entry = Waitlist.objects.create(
            student=request.user.student,
            listing=listing,
            status='Pending'
        )

        # Optionally, you can add a success message
        messages.success(request, 'Application submitted successfully.')

        # Redirect to a relevant page after applying
        return redirect('index')  # You can change 'index' to the appropriate URL

    else:
        # If the request method is not POST, render the page where users can input their application details
        listing = get_object_or_404(Listing, pk=listing_id)
        context = {'listing': listing}
        return render(request, 'application.html', context)
        
@login_required
def request_maintenance(request):
    try:
        occupancy = Occupy.objects.get(student=request.user.student)
        property = occupancy.property
    except Occupy.DoesNotExist:
        messages.error(request, "Check Address.")
        return redirect('maintenance')

    if request.method == 'POST':
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description').strip()

        if not description or not issue_type:
            messages.error(request, 'Issue type and description are required.')
            return render(request, 'Request_Maintenance.html', {'property': property})

        # Create the maintenance request
        RequestMaintenance.objects.create(
            property=property,
            student=request.user.student,
            issue_type=issue_type,
            description=description
        )
        messages.success(request, 'Your maintenance request has been submitted successfully.')
        return redirect('profile')

    # Provide initial form data with property details
    return render(request, 'Request_Maintenance.html', {
        'property': property
    })

def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'FAQ.html', {'faqs': faqs})

from django.shortcuts import redirect, get_object_or_404

@login_required
def delete_application(request, application_id):
    try:
        # Fetch the application
        application = Apply.objects.get(pk=application_id)
        # Ensure that the application belongs to the logged-in user
        if application.student.user != request.user:
            return redirect('show_student_applications')  # Redirect to student applications
        # Delete the application
        application.delete()
    except Apply.DoesNotExist:
        pass  # Handle the case where the application does not exist
    return redirect('show_student_applications')

@login_required
def accept_application(request, application_id):
    try:
        # Fetch the application
        application = get_object_or_404(Apply, pk=application_id)
        # Ensure that the application is associated with a listing owned by the logged-in landlord
        if application.listing.landlord.user != request.user:
            return redirect('show_landlord_applications')  # Redirect to landlord applications
        # Process acceptance logic here
        # For example, you can update the application status to "Accepted"
        application.status = "Accepted"
        application.save()
    except Apply.DoesNotExist:
        pass  # Handle the case where the application does not exist
    return redirect('show_landlord_applications')

@login_required
def reject_application(request, application_id):
    try:
        # Fetch the application
        application = get_object_or_404(Apply, pk=application_id)
        # Ensure that the application is associated with a listing owned by the logged-in landlord
        if application.listing.landlord.user != request.user:
            return redirect('show_landlord_applications')  # Redirect to landlord applications
        # Process rejection logic here
        # For example, you can update the application status to "Rejected"
        application.status = "Rejected"
        application.save()
    except Apply.DoesNotExist:
        pass  # Handle the case where the application does not exist
    return redirect('show_landlord_applications')
