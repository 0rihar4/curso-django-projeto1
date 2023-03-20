import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import AuthorRecipeForm, LoginForm, RegisterForm
from recipes.models import Recipe
from utils.recipes.pagination import make_pagination

# Create your views here.


def register_views(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
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
        user = form.save(commit=False)
        # uma maneira de salvar a senha com criptografia no BD
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Conta criada com sucesso!')

        # apos salvar o usuario na base de dados o ideal é apagar a
        # sessão criada para o registro
        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)  # noqa
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(request, 'Você realizou seu login!')
            login(request, authenticated_user)
            return redirect(reverse('authors:dashboard'))
        else:
            messages.error(request, 'Credenciais invalidas!')
    else:
        messages.error(request, 'Senha ou Login invalidos!')
    return redirect(login_url)


PER_PAGE = int(os.environ.get('PER_PAGE', 9))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    # redirect_field_name='next' seria uma maneira de enviar o usuario para um
    # local onde ele queria acessar mas era necessario estar logado então apos
    # realizar o login, ele sera redirecionado para esta pagina
    if not request.POST:
        return redirect(reverse('authors:login'))
    print('Resultados: ', request.POST, request.user.username)
    if request.POST.get('username') != request.user.username:
        print('Resultados: ', request.POST, request.user.username)
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user,
    ).order_by('-pk')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request,
                  'authors/pages/dashboard.html',
                  context={
                      'recipes': page_obj,
                      'pagination_range': pagination_range,
                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()
    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        request.POST or None,
        instance=recipe,
        files=request.FILES or None
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()
        messages.success(request, 'sua receita foi salva com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(request,
                  'authors/pages/dashboard_recipe.html',
                  context={
                      'recipe': recipe,
                      'form': form,
                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_create_recipe(request):
    form = AuthorRecipeForm(request.POST or None,
                            files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()
        messages.success(request, 'sua receita foi criada com sucesso!')

    return render(request,
                  'authors/pages/dashboard_create_recipe.html',
                  context={
                      'form': form,
                      #   'form_action': reverse('authors:new_recipe_create')
                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    recipe.delete()
    messages.success(request, 'Receita deletada com sucesso!')
    return redirect(reverse('authors:dashboard'))
