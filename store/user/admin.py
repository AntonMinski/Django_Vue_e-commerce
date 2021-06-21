from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'email', 'image_tag']  # 'image_tag'


admin.site.register(UserProfile, UserProfileAdmin)
