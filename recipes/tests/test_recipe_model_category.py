from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.MakeCategory(
            name='Category Testing'
        )
        return super().setUp()

    def test_recipe_category_model_string_representation(self):
        # é possivel colocar mensagens caso a asserção não passe
        self.assertEqual(
            str(self.category),
            self.category.name,
        )

    def test_recipe_category_model_name_max_length_is_hars(self):
        self.category.name ='a'*66
        with self.assertRaises(ValidationError):
            self.category.full_clean()