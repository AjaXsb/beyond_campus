from django.db import models
from django.contrib.auth.models import User

class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.first_name

class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ssn = models.CharField(max_length=20)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.first_name

class RentalAgreement(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    property_id = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    agreement_terms = models.TextField()

    def __str__(self):
        return self.property_id


class Listing(models.Model):
    title = models.CharField(max_length=255)
    rent = models.CharField(max_length=20)
    room = models.CharField(max_length=20)
    amenities = models.CharField(max_length=255)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.listing.title


class Fav(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.student.full_name

class Report(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type

class Waitlist(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status

class Apply(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    application_num = models.IntegerField()
    preferences = models.CharField(max_length=255, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.application_num

class Property(models.Model):
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address

class RentalInsurance(models.Model):
    insurance_email = models.EmailField(unique=True)
    insurance_name = models.CharField(max_length=255, unique=True)


    def __str__(self):
            return self.insurance_name
    
    
class UtilityProvider(models.Model):
    provider_email = models.EmailField(unique=True)
    telephone_number = models.CharField(max_length=20)
    provider_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.provider_name

class Occupy(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.property.address

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.IntegerField()
    
    def __int__(self):
        return self.rating

class UtilityProvide(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    provider = models.ForeignKey(UtilityProvider, on_delete=models.CASCADE)

    def __str__(self):
        return self.provider


class CoveredBy(models.Model):
    insurance = models.ForeignKey(RentalInsurance, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return self.insurance

class RequestMaintenance(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description

class LandlordOwn(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return self.property
