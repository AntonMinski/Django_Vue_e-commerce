from django.contrib.auth.models import User
from django.db import models

from django.utils.safestring import mark_safe

# from webstore.models import Language
# from currencies.models import Currency


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=60)
    email = models.CharField(blank=True, max_length=60)
    shipping_address = models.TextField(blank=True, max_length=600)
    city = models.CharField(blank=True, max_length=40)
    country = models.CharField(blank=True, max_length=50)
    image = models.ImageField(blank=True, upload_to='images/users/')

    # language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True,blank=True)
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True,blank=True)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

    def __str__(self):
        return self.user.username

    def user_name(self):
        user_nm = f'{self.user.first_name} {self.user.last_name} [{self.user.username}]'
        return user_nm

    def image_tag(self):
        img_tag = f'<img src="{self.image.url}" height="50"/>'
        return img_tag

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    image_tag.short_description = 'Image'
