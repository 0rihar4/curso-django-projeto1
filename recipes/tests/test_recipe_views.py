# usar o skip como decorador para pular o teste
# from unittest import skip

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

    def test_recipe_home_template_do_not_load_not_published(self):
        """Test recipe is_published false dont show"""
        self.MakeRecipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<div class="center aviso">',
            response.content.decode('utf-8')
        )

    def test_recipes_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        title_page_category = 'Recipe Title'
        self.MakeRecipe(title=title_page_category)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        # self.assertEqual(response.title, title_page_category)
        content = response.content.decode('utf-8')
        self.assertIn(title_page_category, content)

    def test_recipe_category_template_do_not_load_not_published(self):
        """Test recipe is_published false dont show"""
        # para ter certeza que estou pegando o id de uma categoria criada
        # é necessario atribuir a criação da receita a uma variavel
        recipe = self.MakeRecipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category',
                    kwargs={'category_id': recipe.category.id}))
        self.assertEqual(response.status_code, 404)

    def test_recipes_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipes_detail_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_recipes(self):
        title_detail_page = 'This a detail page - It load one recipe'

        # Need a recipe for this test
        self.MakeRecipe(title=title_detail_page)
        response = self.client.get(reverse('recipes:recipe',
                                           kwargs={'id': 1, }))
        # self.assertEqual(response.title, title_detail_page)
        content = response.content.decode('utf-8')
        self.assertIn(title_detail_page, content)

    def test_recipe_detail_template_do_not_load_not_published(self):
        """Test recipe is_published false dont show"""
        # para ter certeza que estou pegando o id de uma categoria criada
        # é necessario atribuir a criação da receita a uma variavel
        recipe = self.MakeRecipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.pk}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(
            resolved.func, views.search,
            msg='Era esperado a função passada na urls.py para o caminho '
            'recipes:search')

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search')+'?search=a')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        # O meu nesse momento esta diferente do professor por causa que quero
        # exibir uma pagina personalizada
        self.assertEqual(
            response.status_code,
            404
        )
