from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    # é executado antes dos metodos de teste
    def setUp(self) -> None:
        return super().setUp()

    def MakeCategory(self, name='Category'):
        return Category.objects.create(name='Category_teste')

    def MakeAuthor(
            self,
            first_name='user',
            last_name='last',
            username='username',
            password='123456',
            email='email@email.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def MakeRecipe(
            self,
            author_data=None,
            category_data=None,
            title='test_title',
            description='test_description',
            slug='test_slug',
            preparation_time=12,
            preparation_time_unit='test_time_unit',
            servings=2,
            servings_unit='test_serving_unit',
            preparation_steps='test_steps',
            preparation_steps_is_html=False,
            is_published=True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            author=self.MakeAuthor(**author_data),
            category=self.MakeCategory(**category_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
