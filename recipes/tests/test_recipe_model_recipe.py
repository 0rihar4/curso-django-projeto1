from random import randint

from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.MakeRecipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.MakeCategory(name='Test Default Category',),
            author=self.MakeAuthor(username='Test Author',),
            title='test_title',
            description='test_description',
            slug=f'test_slug_{randint(1, 573)}',
            preparation_time=12,
            preparation_time_unit='test_time_unit',
            servings=2,
            servings_unit='test_serving_unit',
            preparation_steps='test_steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_title_raises_error_if_title_has_mores_65_chars(self):
        self.recipe.title = 'C'*66
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # Aqui vamos validar todos os campos que
            # estarão sendo salvos na nossa model antes de enviar para a BD
        # self.recipe.save()  # Aqui salvamos na base de dados, mas se não
        # fosse pelo full_clean o titulo iria com mais de 65 caracteres,
        # o que não é ideal

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_lenght(self, field, max_lenght):
        # para setar um atributo em um objeto ja criado
        # é necessario usar setattr
        setattr(self.recipe, field, 'A'*(max_lenght+1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not false'
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe is_published is not false'
        )

    def test_recipe_string_representation(self):
        title = 'Testing Representation'
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        # é possivel colocar mensagens caso a asserção não passe
        self.assertEqual(
            str(self.recipe), title,
            msg=f'Recipe String representation need to be the same "{title}"'
            f'but "{str(self.recipe)}" was received'
        )
