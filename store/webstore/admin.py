from django.contrib import admin
from .models import Setting, ContactMessage


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at', 'status']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'update_at', 'status', 'short_message']
    readonly_fields = ('name', 'email', 'phone', 'subject', 'product_type',
                       'message', 'ip', )
    list_filter = ['status']


admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
