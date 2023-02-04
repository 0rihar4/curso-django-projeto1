from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def sobre(request):
    # request -> solicitação do cliente
    # response -> respota do servidor
    return render(request, 'recipes/sobre.html', context={
        'name': 'João Vitor',
    })


def home(request):
    # request -> solicitação do cliente
    # response -> respota do servidor
    return render(request, 'recipes/home.html', context={
        'name': 'João Vitor'})


def contato(request):
    # request -> solicitação do cliente
    # response -> respota do servidor
    return render(request, 'me-apague/apague.html')
