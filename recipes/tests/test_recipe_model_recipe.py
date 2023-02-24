from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.MakeRecipe()
        return super().setUp()

    def test_recipe_title_raises_error_if_title_has_mores_65_chars(self):
        self.recipe.title = 'C'*66
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # Aqui vamos validar todos os campos que
            # estarão sendo salvos na nossa model antes de enviar para a BD
        # self.recipe.save()  # Aqui salvamos na base de dados, mas se não
        # fosse pelo full_clean o titulo iria com mais de 65 caracteres,
        # o que não é ideal
