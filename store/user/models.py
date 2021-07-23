from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=60)
    address = models.TextField(blank=True, max_length=600)
    image = models.ImageField(blank=True, upload_to='images/users/')

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

    def __str__(self):
        return self.user.username

    def user_name(self):
        user_nm = f'{self.user.first_name} {self.user.last_name}' \
                  f' [{self.user.username}]'
        return user_nm

    def email(self):
        return self.user.email

    def image_tag(self):
        if not hasattr(self.user, 'image'):
            self.user.image = "images/users/Sample_User_Icon.png"
        img_tag = f'<img src="{self.user.image}" height="50"/>'
        return img_tag

    image_tag.short_description = 'Image'

