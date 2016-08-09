# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from .classes.vk_social import vk_social
from .classes.polls_help import polls_help
from django.conf import settings
from django.core.mail import send_mail
from .forms import PollForm
from .models import Poll, UserSocialProfile, User
from django.http import HttpResponse

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
            polls_help_obj = polls_help()

            if polls_help_obj.is_party_manager(request):
                return redirect('polls.views.polls_list')
            else:
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
                if request.POST['presence'] == '':
                    msg = "bn"
                    form.add_error('presence', msg)
                    return HttpResponse('presence')
                if request.POST['drink'] == '':
                    msg = "nbj"
                    form.add_error('drink', msg)
                    return HttpResponse('drink')
                polls_help_obj = polls_help()
                new_poll_params = polls_help_obj.arrange_poll_form(request, form)
                return render(request, 'polls/new_poll.html', new_poll_params)
        else:
            #find previous
            form = PollForm()
            polls_help_obj = polls_help()
            new_poll_params = polls_help_obj.arrange_poll_form(request, form)
            return render(request, 'polls/new_poll.html', new_poll_params)
    else:
        return redirect('polls.views.login_page')

def polls_list(request):
    polls_help_obj = polls_help()

    if polls_help_obj.is_party_manager(request):
        polls = Poll.objects.order_by('user')
        vk_social_users = UserSocialProfile.objects.order_by('user')
        users = User.objects.all()
        return render(request, 'polls/polls_list.html', {'users': users})
    else:
        return redirect('polls.views.new_poll')