from django.shortcuts import render
from .classes.vk_social import vk_social
from django.http import HttpResponse
from django.conf import settings

def login_page(request):
    return render(request, 'index.html', {'client_id': settings.VK_CLIENT_ID, 'redirect_url': settings.VK_REDIRECT_URL})

def vk_handler(request):
    return HttpResponse(vk_social())
