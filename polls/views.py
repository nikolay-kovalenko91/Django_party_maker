# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from .classes.vk_social import vk_social
from .classes.polls_help import polls_help
from django.conf import settings
from django.core.mail import send_mail
from .forms import PollForm
from .models import User, Poll
from django.contrib.auth import logout
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated():
        polls_help_obj = polls_help()

        if polls_help_obj.is_party_manager(request):
            return redirect('polls.views.polls_list')
        else:
            return redirect('polls.views.new_poll')

    else:
        return redirect('polls.views.login_page')

def login_page(request):
    return render(request, 'auth/login_page.html', {'client_id': settings.VK_CLIENT_ID, 'redirect_url': settings.VK_REDIRECT_URL})

def vk_handler(request):
    if request.method == "GET" and 'code' in request.GET:
        vk_auth_code = request.GET['code']
        vk_user_obj = vk_social(vk_auth_code)
        vk_auth_result = vk_user_obj.register_and_login_user(request)

        if vk_auth_result:
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
        if request.method == "POST":

            if 'next_choice' in request.POST:

                if request.POST['next_choice'] == 'Да':
                    return HttpResponse('yes')
                    '''
                    # send_mail('Новый результат голосования', 'Удален старый и получен новый результат голосования!',settings.EMAIL_HOST_USER, [settings.PARTY_MANAGER_EMAIL])
                    user = request.user
                    poll = Poll.objects.get(user=user)
                    return redirect('polls.views.new_poll')
                    '''
                elif request.POST['next_choice'] == 'Нет':
                    return HttpResponse('no')
                    '''
                    logout(request)
                    return render(request, 'polls/vote_end.html')
                    '''
                else:
                    return HttpResponse('next_choice err')
                    #return redirect('polls.views.new_poll')
            else:
                form = PollForm(request.POST)

                if form.is_valid():
                    poll = form.save(commit=False)
                    poll.user = request.user
                    poll.save()
                    #send_mail('Новый результат голосования', 'Получен новый результат голосования!', settings.EMAIL_HOST_USER, [settings.PARTY_MANAGER_EMAIL])
                    return redirect('')
                else:
                    polls_help_obj = polls_help()
                    new_poll_params = polls_help_obj.arrange_poll_form(request, form)
                    return render(request, 'polls/new_poll.html', new_poll_params)
        else:
            #find previous
            user = request.user
            polls = Poll.objects.filter(user=user)

            if polls:
                return render(request, 'polls/confirm_change_poll.html', {})
            else:
                form = PollForm()
                polls_help_obj = polls_help()
                new_poll_params = polls_help_obj.arrange_poll_form(request, form)
                return render(request, 'polls/new_poll.html', new_poll_params)

    else:
        return redirect('polls.views.login_page')

def polls_list(request):
    polls_help_obj = polls_help()

    if polls_help_obj.is_party_manager(request):

        users = User.objects.all()
        return render(request, 'polls/polls_list.html', {'users': users})
    else:
        return redirect('polls.views.new_poll')

def vote_end(request):
    if request.user.is_authenticated():
        polls_help_obj = polls_help()

        if polls_help_obj.is_party_manager(request):
            return redirect('polls.views.polls_list')
        else:
            logout(request)
            return render(request, 'polls/vote_end.html', {})

    else:
        return redirect('polls.views.login_page')
