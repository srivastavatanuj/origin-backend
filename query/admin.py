from django.contrib import admin
from .models import ContactUs
# Register your models here.


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    # Customize the list display to show relevant fields
    list_display = ('name', 'email', 'subject', 'checked')

    # Enable searching in the admin interface
    search_fields = ('name', 'email', 'subject')

    # Add filters to the right sidebar of the list view
    list_filter = ('checked',)

    # Optionally, you can specify fields to be read-only
    readonly_fields = ('checked',)
