from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils.safestring import mark_safe

# from webstore.models import Language
# from currencies.models import Currency


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=60)
    address = models.TextField(blank=True, max_length=600)
    image = models.ImageField(blank=True, upload_to='images/users/')

    # language = models.ForeignKey(Language,
    # on_delete=models.CASCADE, null=True,blank=True)
    # currency = models.ForeignKey(Currency,
    # on_delete=models.CASCADE, null=True,blank=True)

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

    #
    # def phone(self):
    #     if not hasattr(self.user, 'phone'):
    #         self.user.phone = 'none'
    #     return self.user.phone
    #
    # def address(self):
    #     if not hasattr(self.user, 'address'):
    #         self.user.address = 'none'
    #     return self.user.address

    def image_tag(self):
        if not hasattr(self.user, 'image'):
            self.user.image = "images/users/Sample_User_Icon.png"
        img_tag = f'<img src="{self.user.image}" height="50"/>'
        return img_tag

    image_tag.short_description = 'Image'

    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         UserProfile.objects.create(user=instance)




# class UserProfileForm(ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['user', 'phone', 'email' 'address', 'country', 'image']
