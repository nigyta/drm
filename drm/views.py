from django.shortcuts import render
# from django.http import HttpResponse　# 不要
# from django.template import loader # 不要


def index(request):
    context = {
        'message': "Hello world!!!",
    }
    return render(request, 'drm/index.html', context)

def dashboard(request):
    context = {
        'message': "dashboard page",
    }
    return render(request, 'drm/index.html', context)

def help(request):
    context = {
        'message': "help page",
    }
    return render(request, 'drm/index.html', context)
