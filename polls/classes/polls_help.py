# -*- coding: utf-8 -*-
from django.http import Http404
from ..models import UserSocialProfile
from django.conf import settings
from django.http import Http404

class polls_help():

    def is_party_manager(self, request):
        manager_social_id = settings.PARTY_MANAGER_VK_SOCIAL_ID
        user = request.user
        try:
            social_user = UserSocialProfile.objects.get(user=user)
        except UserSocialProfile.DoesNotExist:
            raise Http404("Такого профиля социальной сети ВКонтакте нет в базе.")

        if social_user.social_id == manager_social_id:
            return True;
        else:
            return None;