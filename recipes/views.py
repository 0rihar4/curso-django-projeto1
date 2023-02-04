from django.shortcuts import render
# Create your views here.


def home(request):
    # request -> solicitação do cliente
    # response -> respota do servidor
    return render(request, 'recipes/pages/home.html', context={
        'name': 'João Vitor'})
