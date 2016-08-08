from django.shortcuts import render, redirect
from .classes.vk_social import vk_social
from django.http import HttpResponse
from django.conf import settings

def login_page(request):
    return render(request, 'index.html', {'client_id': settings.VK_CLIENT_ID, 'redirect_url': settings.VK_REDIRECT_URL})

def vk_handler(request):
    if request.method == "GET" and 'code' in request.GET:
        # CLASS =  init
        vk_auth_code = request.GET['code']
        vk_auth_result = vk_social(vk_auth_code).register_and_login_user(request)
        if vk_auth_result:
            return HttpResponse(vk_social(vk_auth_code).register_and_login_user(request))
    else:
        return redirect('polls.views.login_page')
