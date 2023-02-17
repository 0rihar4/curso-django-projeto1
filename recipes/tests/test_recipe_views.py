# usar o skip como decorador para pular o teste
from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# @skip('mensagem explicando poq pulei o test o wip')
# wip = work in progress
# para um teste sempre falhar escreva self.fail


class RecipeViewsTest(RecipeTestBase):

    # é executado depois dos metodos de teste
    def tearDown(self) -> None:
        return super().tearDown()

    def test_recipes_home_view_function_is_correct(self):
        # Verificando se a funciton view executada na Url: recipes:home
        # é a views.home, mesma ideia segue para os dois proximos testes
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

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
        self.MakeRecipe(author_data={
            'first_name': 'João',
            'last_name': 'Alves',
        }, title='test_title', description='Descrição da Receita')
        response = self.client.get(reverse('recipes:home'))
        # testando o context
        response_recipes = response.context['recipes'].first()
        self.assertEqual(response_recipes.title, 'test_title')
        # Testando o content
        content = response.content.decode('utf-8')
        # Estou verificando se no contet ah os valores que eu passei para criar
        # a receita acima
        self.assertIn('Alves', content)
        self.assertIn('João', content)
        self.assertIn('Descrição da Receita', content)

        pass

    def test_recipes_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipes_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipes_detail_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)
