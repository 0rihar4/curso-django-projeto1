# usar o skip como decorador para pular o teste
# from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# @skip('mensagem explicando poq pulei o test o wip')
# wip = work in progress
# para um teste sempre falhar escreva self.fail


class RecipeCategoryViewTest(RecipeTestBase):

    # é executado depois dos metodos de teste
    def tearDown(self) -> None:
        return super().tearDown()

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
