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

    def test_recipe_search_can_find_recipe_by_title_and_description(self):
        title1 = 'This is recipe one'
        description1 = 'This is description recipe one'
        title2 = 'This is recipe two'
        description2 = 'This is description recipe two'
        recipe1 = self.MakeRecipe(
            slug='one', author_data={'username': 'one'},
            title=title1, description=description1)
        recipe2 = self.MakeRecipe(
            slug='two', author_data={'username': 'two'},
            title=title2, description=description2)

        url = reverse('recipes:search')
        response1 = self.client.get(f'{url}?search={title1}')
        response2 = self.client.get(f'{url}?search={title2}')
        response_both = self.client.get(f'{url}?search=This')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
        print(response_both.context['recipes'])
