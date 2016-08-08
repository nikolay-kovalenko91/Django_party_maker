from django.conf import settings
import requests, time, hashlib, string, random
from ..models import UserSocialProfile, SocialTypes
from django.contrib.auth.models import User
from django.contrib.auth import login

class vk_social():
    '''For the social network'''
    def __init__(self, vk_auth_code):
        # VK authentication step #4
        vk_auth_post_data = {'client_id': settings.VK_CLIENT_ID, 'redirect_uri': settings.VK_REDIRECT_URL,
                             'client_secret': settings.VK_CLIENT_SECRET, 'code': vk_auth_code}
        vk_auth_response = requests.post('https://oauth.vk.com/access_token', data=vk_auth_post_data)

        # VK authentication is OK
        if vk_auth_response.status_code == 200:
            self.vk_auth_json = vk_auth_response.json()
        else:
            self.vk_auth_json = None

    def register_and_login_user(self, request):
        if self.vk_auth_json:
            user_request_post_data = {'user_ids': self.vk_auth_json['user_id'], 'fields': 'photo_100'}
            vk_user_obj = requests.post('https://api.vk.com/method/users.get', data=user_request_post_data)

            try:
                vk_user_json = vk_user_obj.json()['response'][0]
            except:
                return 'err 1'

            # need to be random
            value1 = time.time()
            symbols = string.ascii_letters + string.digits
            value2 = ''.join([random.choice(symbols) for i in range(5)])
            code = hashlib.md5((str(value1) + str(value2)).encode()).hexdigest()

            vk_social_type = SocialTypes.objects.get(name='vk.com')

            #try:
            existing_profile = UserSocialProfile.objects.filter(social_type=vk_social_type,
                                                                social_id=vk_user_json['uid'])

            if (existing_profile):
                user = User.objects.get(usersocialprofile=existing_profile)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            else:
                user = User.objects.create_user(code[-20:])
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                user_social_profile = UserSocialProfile.objects.create(
                        user = request.user, social_type = vk_social_type, social_id = vk_user_json['uid']
                    )
                user_social_profile.social_first_name = vk_user_json['first_name']
                user_social_profile.social_last_name = vk_user_json['last_name']
                user_social_profile.social_photo_url = vk_user_json['photo_100']
                user_social_profile.save()

                return 'ok';
           # except:
            #    return None;
        else:
            return 'err 2';
