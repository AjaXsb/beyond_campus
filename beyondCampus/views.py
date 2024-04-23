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
    context = {}
    user = request.user
    context['user_type'] = 'student' if hasattr(user, 'student') else 'landlord'

    # Retrieve common data for all users
    if context['user_type'] == 'student':
        student = user.student
        context['favorites'] = Fav.objects.filter(student=student)
        context['applications'] = Apply.objects.filter(student=student)
        context['waitlists'] = Waitlist.objects.filter(student=student)
        context['maintenance_requests'] = RequestMaintenance.objects.filter(student=student)

    # Handling POST requests for updates and actions
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            # Handling profile update logic here
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            student.first_name = first_name
            student.last_name = last_name
            student.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('index')

        elif 'submit_request' in request.POST:
            # Handling maintenance request submission
            description = request.POST.get('issue')
            RequestMaintenance.objects.create(property_id=1, student=student,
                                              description=description)  # Adjust property_id as needed
            messages.success(request, "Maintenance request submitted successfully.")
            return redirect('index')

        elif 'submit_report' in request.POST:
            # Handling issue reporting
            report_issue = request.POST.get('reportIssue')
            Report.objects.create(student=student, listing_id=1, type=report_issue)  # Adjust listing_id as needed
            messages.success(request, "Issue reported successfully.")
            return redirect('index')
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
@login_required
def profile(request):

    properties = None  # Define properties variable outside the try-except block

    try:
        # Try to fetch a Student object associated with the user
        user_info = Student.objects.get(user=request.user)
        user_type = 'student'

    except Student.DoesNotExist:
        try:
            # Try to fetch a Landlord object associated with the user
            user_info = Landlord.objects.get(user=request.user)
            user_type = 'landlord'
            properties = Property.objects.filter(landlordown__landlord=user_info)
            print(properties)

        except Landlord.DoesNotExist:
            # Handle the case where the user does not have a Student or Landlord object
            user_info = None
            user_type = None
            
    return render(request, "profile.html", {"user_info": user_info, "user_type": user_type, "properties": properties})

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    reviews = Review.objects.filter(property_id=listing.property_id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews.exists() else "No ratings yet"

    if request.method == 'POST':
        if 'add_fav' in request.POST:
            # Assuming the user is logged in and is a student
            Fav.objects.create(student=request.user.student, listing=listing)
            return redirect('listing_detail', listing_id=listing_id)  # Redirect back to the same listing page

    context = {
        'listing': listing,
        'average_rating': average_rating,
    }
    return render(request, 'listing.html', context)


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

def myhouse_dashboard(request):
    # Assuming each user is linked to a student and each student is linked to exactly one property
    student = get_object_or_404(Student, user=request.user)
    property = get_object_or_404(Property, student=student)

    context = {
        'property': property,
    }
    return render(request, 'myhouse_dashboard.html', context)

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
def show_applications(request):
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

    return render(request, 'show_applications.html', data)
    
    
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

@login_required
def application_submission(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            new_application = form.save(commit=False)

            student = Student.objects.get(id=request.POST.get('student_id'))
            listing = Listing.objects.get(id=request.POST.get('listing_id'))
            new_application.student = student
            new_application.listing = listing

            new_application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('applications')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ApplicationForm()
    return render(request, 'application.html', {'form': form})

@login_required
def create_maintenance_request(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        landlord_name = request.POST.get('landlord_name')
        request_type = request.POST.get('request_type')
        issue_description = request.POST.get('issue')
        rental_address = request.POST.get('rental_address')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        try:
                student = request.user.student
            except Student.DoesNotExist:
                return HttpResponse("You do not have a student profile.", status=400)
        try:
            occupy_record = Occupy.objects.get(student=student)
            property = occupy_record.property
        except Occupy.DoesNotExist:
                return HttpResponse("You do not have a registered property.", status=400)
        
        if not validate_address_with_property(property, rental_address, address2, city, state, zip_code):
            return HttpResponse("The provided address does not match our records.", status=400)
