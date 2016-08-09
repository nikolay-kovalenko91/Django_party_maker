from django.contrib import admin
from .models import SocialTypes, UserSocialProfile, Poll

admin.site.register(SocialTypes)
admin.site.register(UserSocialProfile)
admin.site.register(Poll)