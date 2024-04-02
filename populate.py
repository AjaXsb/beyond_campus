import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")
django.setup()

from django.contrib.auth.models import User
from beyondCampus.models import University, Student, Landlord, RentalAgreement, Listing, Image, Fav, Report, Waitlist, Apply, Property, RentalInsurance, UtilityProvider, Occupy, Review, UtilityProvide, CoveredBy, RequestMaintenance, LandlordOwn

# Create at least 10 University instances
for i in range(1, 11):
    University.objects.create(name=f'University {i}', location=f'Location {i}')

# Create at least 10 Student instances
for i in range(1, 11):
    user = User.objects.create(username=f'student{i}')
    Student.objects.create(user=user, full_name=f'Student {i}', phone=f'Phone {i}', address=f'Address {i}', university_id=i)

# Create at least 10 Landlord instances
for i in range(1, 11):
    user = User.objects.create(username=f'landlord{i}')
    Landlord.objects.create(user=user, ssn=f'SSN {i}', full_name=f'Landlord {i}')

# Create at least 10 RentalAgreement instances
for i in range(1, 11):
    landlord = Landlord.objects.get(id=i)
    student = Student.objects.get(id=i)
    RentalAgreement.objects.create(landlord=landlord, student=student, property_id=i, start_date=f'2024-01-{i}', end_date=f'2024-12-{i}', rent_amount=i*100, agreement_terms=f'Agreement Terms {i}')

# Create at least 10 Listing instances
for i in range(1, 11):
    landlord = Landlord.objects.get(id=i)
    Listing.objects.create(title=f'Listing {i}', rent=f'Rent {i}', room=f'Room {i}', amenities=f'Amenities {i}', landlord=landlord)

# Create at least 10 Image instances
for i in range(1, 11):
    listing = Listing.objects.get(id=i)
    Image.objects.create(listing=listing)

# Create at least 10 Fav instances
for i in range(1, 11):
    student = Student.objects.get(id=i)
    listing = Listing.objects.get(id=i)
    Fav.objects.create(student=student, listing=listing)

# Create at least 10 Report instances
for i in range(1, 11):
    student = Student.objects.get(id=i)
    listing = Listing.objects.get(id=i)
    Report.objects.create(student=student, listing=listing, type=f'Type {i}')

# Create at least 10 Waitlist instances
for i in range(1, 11):
    student = Student.objects.get(id=i)
    listing = Listing.objects.get(id=i)
    Waitlist.objects.create(student=student, listing=listing, status=f'Status {i}')

# Create at least 10 Apply instances
for i in range(1, 11):
    student = Student.objects.get(id=i)
    listing = Listing.objects.get(id=i)
    Apply.objects.create(student=student, listing=listing, application_num=i)

# Create at least 10 Property instances
for i in range(1, 11):
    Property.objects.create(address=f'Address {i}')

# Create at least 10 RentalInsurance instances
for i in range(1, 11):
    RentalInsurance.objects.create(insurance_email=f'email{i}@example.com', insurance_name=f'Insurance {i}')

# Create at least 10 UtilityProvider instances
for i in range(1, 11):
    UtilityProvider.objects.create(provider_email=f'email{i}@example.com', telephone_number=f'Phone {i}', provider_name=f'Provider {i}')

# Create at least 10 Occupy instances
for i in range(1, 11):
    property = Property.objects.get(id=i)
    student = Student.objects.get(id=i)
    Occupy.objects.create(property=property, student=student)

# Create at least 10 Review instances
for i in range(1, 11):
    property = Property.objects.get(id=i)
    student = Student.objects.get(id=i)
    Review.objects.create(property=property, student=student, rating=i)

# Create at least 10 UtilityProvide instances
for i in range(1, 11):
    property = Property.objects.get(id=i)
    provider = UtilityProvider.objects.get(id=i)
    UtilityProvide.objects.create(property=property, provider=provider)

# Create at least 10 CoveredBy instances
for i in range(1, 11):
    insurance = RentalInsurance.objects.get(id=i)
    property = Property.objects.get(id=i)
    CoveredBy.objects.create(insurance=insurance, property=property)

# Create at least 10 RequestMaintenance instances
for i in range(1, 11):
    property = Property.objects.get(id=i)
    student = Student.objects.get(id=i)
    RequestMaintenance.objects.create(property=property, student=student, description=f'Description {i}')

# Create at least 10 LandlordOwn instances
for i in range(1, 11):
    landlord = Landlord.objects.get(id=i)
    property = Property.objects.get(id=i)
    LandlordOwn.objects.create(landlord=landlord, property=property)

