from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'template1/index.html')

def imagem(request):
    return render(request, 'template1/imagem.html')