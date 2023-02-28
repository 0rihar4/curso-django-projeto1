from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

# from utils.recipes.factory import make_recipe
from .models import Recipe

# Create your views here.


def home(request):
    # request -> solicitação do cliente
    # response -> respota do servidor
    recipes = Recipe.objects.all().filter(
        is_published=True,
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
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
    search_term = request.GET.get('search')
    if not search_term:
        raise Http404()
    return render(request, 'recipes/pages/search.html')
