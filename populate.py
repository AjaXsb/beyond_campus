import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")
django.setup()

import random
from faker import Faker
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
# Manual entries for listing titles
listing_titles = [
    "Cozy Apartment near University Campus",
    "Spacious Loft with City View for Students",
    "Charming House for Student Living",
    "Modern Studio in Student-Friendly Area",
    "Luxury Condo Perfect for Student Lifestyle",
    "Elegant Townhouse for University Students",
    "Rustic Cabin Retreat for Student Getaways",
    "Contemporary Penthouse with Campus Proximity",
    "Quaint Cottage Ideal for Student Accommodation",
    "Sleek Apartment with Easy Access to University"
]

for title in listing_titles:
    landlord = random.choice(Landlord.objects.all())
    listing = Listing.objects.create(
        title=title,
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

# Create FAQs with real-world sample questions and answers
faqs = [
    {"question": "How do I apply for housing?", "answer": "You can apply for housing by filling out the application form available on our website."},
    {"question": "What amenities are included in the rent?", "answer": "Amenities such as water, electricity, and internet are typically included in the rent. Please refer to the specific listing for details."},
    {"question": "Can I bring pets?", "answer": "Some listings allow pets with an additional pet deposit. Please check with the landlord for their pet policy."},
    {"question": "Is parking available?", "answer": "Parking availability varies by listing. Some properties offer on-site parking, while others may have street parking available. Check the listing details for parking information."},
    {"question": "Are utilities included in the rent?", "answer": "In some cases, utilities such as water and electricity may be included in the rent. However, it's essential to review the listing details for information on utilities."},
    {"question": "How do I report maintenance issues?", "answer": "You can report maintenance issues by contacting the landlord or property management directly. Alternatively, you can submit a maintenance request through our website."},
    {"question": "What is the lease duration?", "answer": "Lease durations vary by listing. Some properties offer month-to-month leases, while others may require a one-year commitment. Review the lease terms in the listing details for more information."},
    {"question": "Can I sublease my apartment?", "answer": "Subleasing policies vary by landlord and property. Please consult the lease agreement and discuss with the landlord if subleasing is allowed."},
    {"question": "How do I pay rent?", "answer": "Rent payment methods vary by landlord. Some accept online payments, while others may require checks or money orders. Check with your landlord for their preferred payment method."},
    {"question": "What is the security deposit amount?", "answer": "The security deposit amount is typically one month's rent. However, it may vary depending on the listing and landlord requirements."},
]

for faq in faqs:
    FAQ.objects.create(
        question=faq["question"],
        answer=faq["answer"]
    )

print("Data populated successfully!")