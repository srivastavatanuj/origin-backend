from django.contrib import admin, messages
from django import forms
from .models import User, ClientBusiness, StaffProfile, ClientCataloge, ClientAddress
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings



class UserChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm

    list_display = ('email', 'full_name', 'phone',
                    'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name', 'phone')
    ordering = ('email',)
    readonly_fields = ('last_login',)

    fieldsets = (
        ('Login Info', {'fields': ('email',)}),
        ('Personal Info', {'fields': ('full_name', 'nick_name', 'phone')}),
        ('Status & Permissions', {
         'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Last Login', {'fields': ('last_login',)}),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new user
            password = get_random_string(length=10)
            obj.set_password(password)
            obj.save()

            subject = 'Origins Coffee Account Created'
            message = f"Hello {obj.full_name},\n\nYour account has been created.\nYour password is: {password}\n\nPlease change your password after logging in."
            recipient_list = [obj.email]
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    recipient_list,
                    fail_silently=False,
                )
                messages.success(request, f"User created successfully. Password sent to {obj.email}")
            except Exception as e:
                messages.error(request, f"User created, but failed to send email: {str(e)}")
        else:
            super().save_model(request, obj, form, change)


    def response_add(self, request, obj, post_url_continue=None):
        if not obj.is_staff:
            url = reverse('admin:buyers_clientbusiness_add') + \
                f'?user={obj.pk}'
            return HttpResponseRedirect(url)
        return super().response_add(request, obj, post_url_continue)


class ClientBusinessAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'account_number',
                    'business_email', 'sales_rep')
    search_fields = ('business_name', 'account_number', 'business_email')

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        user_id = request.GET.get("user")
        if user_id:
            initial['user'] = user_id  # assuming `user` is the FK field name
        return initial

    def response_add(self, request, obj, post_url_continue=None):
        url = reverse('admin:buyers_clientcataloge_add') + \
            f'?user={obj.user.pk}'
        return HttpResponseRedirect(url)


class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__full_name',)


class ClientCatalogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name',
                    'order_frequency', 'pricing_enabled')
    search_fields = ('user__email',)

    def business_name(self, obj):
        return ClientBusiness.objects.get(user=obj.user).business_name

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        user_id = request.GET.get("user")
        if user_id:
            initial['user'] = user_id  # assuming `user` is the FK field name
        return initial

    def response_add(self, request, obj, post_url_continue=None):
        if ClientBusiness.objects.filter(user=obj.user).exists():
            return super().response_add(request, obj, post_url_continue)

        url = reverse('admin:buyers_clientbusiness_add') + \
            f'?user={obj.user.id}'
        return HttpResponseRedirect(url)

    def save_model(self, request, obj, form, change):
        user = form.cleaned_data['user']
        if ClientBusiness.objects.filter(user=user).exists():
            super().save_model(request, obj, form, change)
        else:
            messages.error(
                request, f"Cannot save catalog: {user.email} Client Business not found.")


class ClientAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'billing_city', 'billing_state',
                    'shippingSameAsBilling')
    search_fields = ('user__email', 'billing_city', 'billing_state')


admin.site.register(User, UserAdmin)
admin.site.register(ClientBusiness, ClientBusinessAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(ClientAddress, ClientAddressAdmin)
admin.site.register(ClientCataloge, ClientCatalogeAdmin)
