from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    # def test_the_pytest_ok(self):
    #     assert 1 == 1, 'Um é igual a Um'

    def test_recipes_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipes_category_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipes_recipe_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'pk': 1})
        self.assertEqual(url, '/recipes/1/')

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')

    def test_recipe_search_term_is_on_page_and_espade(self):
        url = reverse('recipes:search') + '?search="teste"'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;teste&quot;',
            response.content.decode('utf-8')
        )
