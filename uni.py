import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
import django
django.setup()

from django.conf import settings
import pandas as pd
from beyondCampus.models import University

def import_universities_from_excel(file_path):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        name = row['Name']
        location = row['County name']
        # Check if the university already exists
        if not University.objects.filter(name=name).exists():
            University.objects.create(name=name, location=location)
        else:
            # University already exists, update location if needed
            university = University.objects.get(name=name)
            university.location = location
            university.save()

# Example usage:
file_path = r'D:\Chikku\Docs\Code\DBMS\Proj\beyond_campus\Universities_list.xlsx'
import_universities_from_excel(file_path)