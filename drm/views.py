from django.shortcuts import render
from drm.models import Protein


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

def list_proteins(request):
    """Proteinの一覧"""
    proteins = Protein.objects.all().order_by('id')
    context = {
        'proteins': proteins,
        'message': "Protein List"
    }

    return render(request, 'drm/list_proteins.html', context)
