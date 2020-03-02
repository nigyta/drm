from django.shortcuts import render, get_object_or_404
from drm.models import Protein
from django.contrib import messages

def index(request):
    messages.success(request, 'message test')
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
    proteins = Protein.objects.all().order_by('id')[:100] # debug用に先頭100件のみ
    context = {
        'proteins': proteins,
        'message': "Protein List"
    }
    return render(request, 'drm/list_proteins.html', context)

def ref_detail(request, ref_id):
    protein = get_object_or_404(Protein, ref_id=ref_id)
    context = {
        'message': f"{protein.ref_id}: {protein.description} ({protein.organism})"
    }
    return render(request, 'drm/index.html', context)