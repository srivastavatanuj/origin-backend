from django.contrib import admin
from .models import QuickBooksToken, QuickBooksLog
from django.utils.html import format_html
from django.urls import path
from django.contrib import messages
from django.shortcuts import redirect


@admin.register(QuickBooksToken)
class QuickBooksTokenAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=...):
        return False

    list_display = ('realm_id', 'last_refreshed', 'expires_in',
                    'x_refresh_token_expires_in', 'renew_token_button')

    # def get_urls(self):
    #     urls = super().get_urls()
    #     return urls

    def renew_token_button(self, obj):
        return format_html(
            '<a class="button" target="_blank" href="{}">Renew</a>',
            "/quickbook/login/"
        )
    renew_token_button.short_description = "Renew Token"
    renew_token_button.allow_tags = True


@admin.register(QuickBooksLog)
class QuickBooksLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'event_type', 'status')
    search_fields = ('event_type', 'status')
