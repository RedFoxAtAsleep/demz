from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return HttpResponse('Welcome to someapp.')


def download(request):
    if request.method == 'GET':
        return HttpResponse('POST ONLY.')
    if request.method == 'POST':
        pass


