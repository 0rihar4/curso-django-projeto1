import os

from django.db.models import Q
from django.http import Http404
from django.views.generic import DetailView, ListView

from recipes.models import Recipe
from utils.recipes.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 9))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    # get_queryset é usado para manipular as queryset usadas para fazer
    # pesquisas e filtros na base de dados
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(
            is_published=True
        )

        return qs

    # o get_context_data é usado para manipular os contexts que enviamos para
    # os templates, assim possibilitando adicionar paginação, enviar variaveis
    # para o contexto e etc
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, ctx.get('recipes'), PER_PAGE)
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(
            is_published=True,
            category__id=self.kwargs.get('category_id')
        )
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update(
            {
                'title': f'{ctx.get("recipes")[0].category.name} - Category |'
            }
        )
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('search', '')
        if not search_term:
            raise Http404()
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('search', '').strip()
        ctx.update(
            {
                'page_title': f'Search for {search_term} |',
                'search_term': search_term,
                'additional_url_query': f'&search={search_term}'
            }
        )
        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/single-recipe.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(
            is_published=True,
        )
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update(
            {
                'is_detail_page': True,
            }
        )
        return ctx
