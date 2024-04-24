import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")
django.setup()

import random
from faker import Faker
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User
from beyondCampus.models import University, Student, Landlord, RentalAgreement, Listing, Image, Fav, Report, Waitlist, Apply, Property, RentalInsurance, UtilityProvider, Occupy, FAQ, Review, UtilityProvide, CoveredBy, RequestMaintenance, LandlordOwn

fake = Faker()
# Create Users and link to Students and Landlords
for _ in range(40):
    user = User.objects.create_user(
        username=fake.user_name(),
        email=fake.email(),
        password="password"
    )
    Student.objects.create(
        user=user,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone=fake.phone_number(),
        address=fake.address(),
        university=random.choice(University.objects.all())
    )
    Landlord.objects.create(
        user=user,
        ssn=fake.ssn(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone=fake.phone_number(),
        address=fake.address()
    )

# Create RentalAgreements
for _ in range(20):
    RentalAgreement.objects.create(
        landlord=random.choice(Landlord.objects.all()),
        student=random.choice(Student.objects.all()),
        property_id=random.randint(1000, 9999),
        start_date=fake.date_between(start_date="-1y", end_date="today"),
        end_date=fake.date_between(start_date="today", end_date="+1y"),
        rent_amount=random.randint(500, 2000),
        agreement_terms=fake.text()
    )

# Create Listings and Images
for _ in range(20):
    landlord = random.choice(Landlord.objects.all())
    listing = Listing.objects.create(
        title=fake.text(max_nb_chars=50),
        rent=str(random.randint(500, 2000)),
        room=str(random.randint(1, 5)),
        amenities=fake.text(max_nb_chars=100),
        landlord=landlord
    )
    Image.objects.create(listing=listing)

# Create Favs
for _ in range(20):
    Fav.objects.create(
        student=random.choice(Student.objects.all()),
        listing=random.choice(Listing.objects.all())
    )

# Create Reports
for _ in range(20):
    Report.objects.create(
        student=random.choice(Student.objects.all()),
        listing=random.choice(Listing.objects.all()),
        type=random.choice(["Maintenance", "Safety", "Noise"])
    )

# Create Waitlists
for _ in range(20):
    Waitlist.objects.create(
        student=random.choice(Student.objects.all()),
        listing=random.choice(Listing.objects.all()),
        status=random.choice(["Pending", "Approved", "Rejected"])
    )

# Create Applications
for _ in range(20):
    Apply.objects.create(
        student=random.choice(Student.objects.all()),
        listing=random.choice(Listing.objects.all()),
        application_num=random.randint(1000, 9999),
        preferences=fake.text(max_nb_chars=100),
        additional_info=fake.text()
    )

# Create Properties
for _ in range(20):
    Property.objects.create(
        address=fake.address()
    )

# Create RentalInsurances
for _ in range(20):
    RentalInsurance.objects.create(
        insurance_email=fake.email(),
        insurance_name=fake.company()
    )

# Create UtilityProviders
for _ in range(20):
    UtilityProvider.objects.create(
        provider_email=fake.email(),
        telephone_number=fake.phone_number(),
        provider_name=fake.company()
    )

# Create Occupies
for _ in range(20):
    Occupy.objects.create(
        property=random.choice(Property.objects.all()),
        student=random.choice(Student.objects.all())
    )

# Create Reviews
for _ in range(20):
    Review.objects.create(
        property=random.choice(Property.objects.all()),
        student=random.choice(Student.objects.all()),
        rating=random.randint(1, 5)
    )

# Create UtilityProvides
for _ in range(20):
    UtilityProvide.objects.create(
        property=random.choice(Property.objects.all()),
        provider=random.choice(UtilityProvider.objects.all())
    )

# Create CoveredBys
for _ in range(20):
    CoveredBy.objects.create(
        insurance=random.choice(RentalInsurance.objects.all()),
        property=random.choice(Property.objects.all())
    )

# Create RequestMaintenances
for _ in range(20):
    RequestMaintenance.objects.create(
        property=random.choice(Property.objects.all()),
        student=random.choice(Student.objects.all()),
        issue_type=random.choice(["Plumbing", "Electrical", "General"]),
        description=fake.text()
    )

# Create LandlordOwns
for _ in range(20):
    LandlordOwn.objects.create(
        landlord=random.choice(Landlord.objects.all()),
        property=random.choice(Property.objects.all())
    )

# Create FAQs
for _ in range(20):
    FAQ.objects.create(
        question=fake.text(max_nb_chars=100),
        answer=fake.text()
    )

print("Data populated successfully!")