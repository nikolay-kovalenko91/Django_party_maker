# -*- coding: utf-8 -*-
from django.http import Http404
from ..models import UserSocialProfile, Poll
from ..forms import PollForm
from django.conf import settings
from django.http import Http404

class polls_help():

    def is_party_manager(self, request):
        '''To find out if user manager of the app or not'''
        manager_social_id = settings.PARTY_MANAGER_VK_SOCIAL_ID
        user = request.user
        # find the profile
        try:
            social_user = UserSocialProfile.objects.get(user=user)
        except:
            raise Http404("Такого профиля социальной сети ВКонтакте нет в базе.")

        if social_user.social_id == manager_social_id:
            return True
        else:
            return None

    def arrange_poll_form(self, request, form):
        '''To arrange params for the poll form'''
        user = request.user
        try:
            vk_social_user = UserSocialProfile.objects.get(user=user)
        except:
            raise Http404("Такого профиля социальной сети ВКонтакте нет в базе.")
        return {'form': form, 'vk_social_user': vk_social_user}