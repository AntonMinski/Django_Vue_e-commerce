from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'phone', 'email', 'city', 'country',
                    'image_tag']  # 'language', 'currency'


admin.site.register(UserProfile, UserProfileAdmin)
