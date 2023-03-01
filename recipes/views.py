from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.recipes.pagination import make_pagination_range

# from utils.recipes.factory import make_recipe
from .models import Recipe

# Create your views here.


def home(request):
    # request -> solicitação do cliente
    # response -> respota do servidor
    recipes = Recipe.objects.all().filter(
        is_published=True,
    ).order_by('-id')
    current_page = request.GET.get('page', 1)
    paginator = Paginator(recipes, 9)
    page_object = paginator.get_page(current_page)
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_object,
    })


def category(request, category_id):
    # request -> solicitação do cliente
    # response -> respota do servidor
    # é possivel passar uma query pronta dentro do get_list_or_404
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    # category_name = getattr(recipes.first(), 'category', None)
    # recipes get_list_or_404(
    #     # Model escolhido
    #     Recipe,
    #     # Filtros para a query
    #     category__id=category_id,is_published=True,
    #     )
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name}',
    })


def recipe(request, id):
    # recipe = Recipe.objects.filter(
    #     pk=id,
    #     is_published=True,
    # ).order_by('-id').first()
    recipe = get_object_or_404(Recipe, pk=id,
                               is_published=True,)
    return render(request, 'recipes/pages/single-recipe.html', context={
        'recipe': recipe,
        'is_detail_page': True})


def search(request):
    search_term = request.GET.get('search', '').strip()
    if not search_term:
        raise Http404()
    # Recipe.objects.get() -> pega 1 valor
    # Recipe.objects.all() -> pega todos os valores
    # Q -> troca o AND situacional de um filter comum por OR
    recipes = Recipe.objects.filter(
        # __icontains -> procura valores semelhantes ao termo independente
        # da letra maiuscula e minuscula
        # __contains -> procura valores semelhantes ao termo levando em conta
        # letra maiuscula e minuscula
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True,
    ).order_by('-id')
    # Para evitar querys longas é possivel fazelas separadas tbm como abaixo
    # recipes = recipes.filter(
    #     is_published=True,
    # )
    # recipes = recipes.order_by('-id')
    # Para ver a query que ta sendo consultada no console de depuração
    # basta colocar str(recipes.query)
    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for {search_term} |',
        'search_term': search_term,
        'recipes': recipes
    })
