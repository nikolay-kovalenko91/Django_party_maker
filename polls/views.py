from django.shortcuts import render, redirect, get_object_or_404
from .classes.vk_social import vk_social
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from .forms import PollForm
from .models import Poll, UserSocialProfile


def login_page(request):
    return render(request, 'auth/login_page.html', {'client_id': settings.VK_CLIENT_ID, 'redirect_url': settings.VK_REDIRECT_URL})

def vk_handler(request):
    if request.method == "GET" and 'code' in request.GET:
        # CLASS =  init
        vk_auth_code = request.GET['code']
        vk_user_obj = vk_social(vk_auth_code)
        vk_auth_result = vk_user_obj.register_and_login_user(request)

        if vk_auth_result:
            # !!!!!!!!!
            return redirect('polls.views.new_poll')
        else:
            # auth error !!!!
            return redirect('polls.views.login_page')
    else:
        return redirect('polls.views.login_page')

def new_poll(request):
    if request.user.is_authenticated():
        #send_mail('New', 'Hey test test', settings.EMAIL_HOST_USER, ['party.maker.adm@yandex.ru'])
        if request.method == "POST":
            form = PollForm(request.POST)
            if form.is_valid():
                poll = form.save(commit=False)
                poll.user = request.user
                poll.save()
                # !!! THANK u form
                return redirect('/')
        else:
            #find previous
            user = request.user
            polls = Poll.objects.filter(user=user)
            if polls:
                poll_is_exist = True
            else:
                poll_is_exist = False
            form = PollForm()
            social_user = get_object_or_404(UserSocialProfile, user=user, title='Такого профиля социальной сети ВКонтакте нет в базе')
            return render(request, 'polls/new_poll.html', {'form': form, 'social_user': social_user})
    else:
        return redirect('polls.views.login_page')

def polls_list(request):
    manager_social_id = settings.PARTY_MANAGER_VK_SOCIAL_ID
    user = request.user
    social_user =  get_object_or_404(UserSocialProfile, user=user, title='Такого профиля социальной сети ВКонтакте нет в базе')

    if social_user.social_id == manager_social_id:
        polls = Poll.objects.order_by('user')
        return render(request, 'polls/polls_list.html', {'polls': polls})
    else:
        return redirect('polls.views.new_poll')