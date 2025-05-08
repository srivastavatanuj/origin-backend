from django.contrib import admin
from buyers.models import User, ClientBusiness, StaffProfile, ClientAddress, ClientCataloge
# Register your models here.
admin.site.register(User)
admin.site.register(ClientBusiness)
admin.site.register(StaffProfile)
admin.site.register(ClientAddress)
admin.site.register(ClientCataloge)
