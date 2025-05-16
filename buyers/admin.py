from django.contrib import admin
from .models import User, ClientBusiness, StaffProfile, ClientCataloge, ClientAddress


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'phone',
                    'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name', 'phone')
    ordering = ('email',)
    readonly_fields = ('last_login',)

    fieldsets = (('Login Info', {'fields': ('email', 'password')}), ('Personal Info', {'fields': ('full_name',
                                                                                                  'nick_name', 'phone')}), ('Status & Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                                                                                                                                                'groups', 'user_permissions')}), ('Extra Info', {'fields': ('hash', 'timestamp', 'last_login')}))


class ClientBusinessAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'account_number',
                    'business_email', 'sales_rep')
    search_fields = ('business_name', 'account_number', 'business_email')


class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__full_name',)


class ClientCatalogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_frequency', 'pricing_enabled')
    search_fields = ('user__email',)


class ClientAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'billing_city', 'billing_state',
                    'shippingSameAsBilling')
    search_fields = ('user__email', 'billing_city', 'billing_state')


admin.site.register(User, UserAdmin)
admin.site.register(ClientBusiness, ClientBusinessAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(ClientAddress, ClientAddressAdmin)
admin.site.register(ClientCataloge, ClientCatalogeAdmin)
