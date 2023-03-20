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

    def test_recipes_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 21}))
        self.assertIs(view.func.view_class, views.RecipeDetail)

    def test_recipes_detail_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_recipes(self):
        title_detail_page = 'This a detail page - It load one recipe'

        # Need a recipe for this test
        self.MakeRecipe(title=title_detail_page)
        response = self.client.get(reverse('recipes:recipe',
                                           kwargs={'pk': 1, }))
        # self.assertEqual(response.title, title_detail_page)
        content = response.content.decode('utf-8')
        self.assertIn(title_detail_page, content)

    def test_recipe_detail_template_do_not_load_not_published(self):
        """Test recipe is_published false dont show"""
        # para ter certeza que estou pegando o id de uma categoria criada
        # é necessario atribuir a criação da receita a uma variavel
        recipe = self.MakeRecipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 404)
