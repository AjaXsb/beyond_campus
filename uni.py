import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
import django
django.setup()

from django.conf import settings

# Set the DJANGO_SETTINGS_MODULE environment variable


# Manually configure Django settings


import csv
from beyondCampus.models import University

def import_universities_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['University Name']
            location = row['State']
            # Check if the university already exists
            if not University.objects.filter(name=name).exists():
                University.objects.create(name=name, location=location)
            else:
                # University already exists, update location if needed
                university = University.objects.get(name=name)
                university.location = location
                university.save()

# Example usage:
file_path = r'D:\Chikku\Docs\Code\DBMS\Proj\US-News-Rankings-Universities-Through-2023.csv'
import_universities_from_csv(file_path)