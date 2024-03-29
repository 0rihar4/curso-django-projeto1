# usar o skip como decorador para pular o teste
# from unittest import skip

from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# @skip('mensagem explicando poq pulei o test o wip')
# wip = work in progress
# para um teste sempre falhar escreva self.fail


class RecipeHomeViewTest(RecipeTestBase):

    # é executado depois dos metodos de teste
    def tearDown(self) -> None:
        return super().tearDown()

    def test_recipes_home_view_function_is_correct(self):
        # Verificando se a funciton view executada na Url: recipes:home
        # é a views.home, mesma ideia segue para os dois proximos testes
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    # testando se ao acessar a url home o status code retornado é 200
    def test_recipe_home_view_return_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    # testando se o template executado na url recipes:home
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        # testando a pagina recipes-not-found da home
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<div class="center aviso">',
            response.content.decode('utf-8')
        )

    # Teste qe verifica se o template da home esta renderizando as receitas
    def test_recipe_home_template_loads_recipes(self):
        self.MakeRecipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('test_title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_do_not_load_not_published(self):
        """Test recipe is_published false dont show"""
        self.MakeRecipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<div class="center aviso">',
            response.content.decode('utf-8')
        )

    def test_recipe_home_is_paginated(self):
        # é possivel fazer com decorator
        # @patch('recipes.views.PER_PAGE', new=3)
        for i in range(8):
            kwargs = {'author_data': {'username': f'u{i}'}, 'slug': f'r{i}'}
            self.MakeRecipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            # Como o pagination esta vinculado ao nosso contexto conseguimos
            # acessar ele e suas informações como qntd por pagina, num de paginas # noqa:E501
            pagination = recipes.paginator

            self.assertEqual(pagination.num_pages, 1)
            self.assertEqual(len(pagination.get_page(1)), 8)
            self.assertEqual(len(pagination.get_page(2)), 8)
            self.assertEqual(len(pagination.get_page(3)), 8)

    def test_invalid_page_query_uses_page_1(self):
        for i in range(8):
            kwargs = {'author_data': {'username': f'u{i}'}, 'slug': f'r{i}'}
            self.MakeRecipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home')+'?page=aaaa')
            self.assertEqual(response.context['recipes'].number, 1)

            response = self.client.get(reverse('recipes:home')+'?page=8')
            self.assertEqual(response.context['recipes'].number, 1)
