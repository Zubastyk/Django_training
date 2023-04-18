from django.shortcuts import render

from .models import Bb


def index(request):
    bbs = Bb.objects.all()
    return render(request, 'index.html', {'bbs':bbs})