from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import RegisterForm

# Create your views here.


def register_views(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form
    })


def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)  # noqa

    if form.is_valid():
        # is_valid() pega o formulario e ve se tdos os campos passaram
        # se sim, passara no if e sera salvo na base de dados
        form.save()
        messages.success(request, 'Conta criada com sucesso!')

        # apos salvar o usuario na base de dados o ideal é apagar a
        # sessão criada para o registro
        del (request.session['register_form_data'])

    return redirect('authors:register')
