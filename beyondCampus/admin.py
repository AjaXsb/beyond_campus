from django.contrib import admin


from .models import University, UtilityProvider, UtilityProvide,Apply,RentalAgreement,Student,Landlord,LandlordOwn,Listing,Fav,Image,RentalInsurance,Report,RequestMaintenance,Review,Waitlist,Property,Occupy,CoveredBy
admin.site.register(UtilityProvider)
admin.site.register(UtilityProvide)

admin.site.register(University)
admin.site.register(Apply)
admin.site.register(RentalAgreement)
admin.site.register(RentalInsurance)
admin.site.register(Student)
admin.site.register(Landlord)
admin.site.register(LandlordOwn)
admin.site.register(Listing)
admin.site.register(Fav)
admin.site.register(Image)
admin.site.register(Report)
admin.site.register(RequestMaintenance)
admin.site.register(Review)
admin.site.register(Waitlist)
admin.site.register(Property)
admin.site.register(Occupy)
admin.site.register(CoveredBy)