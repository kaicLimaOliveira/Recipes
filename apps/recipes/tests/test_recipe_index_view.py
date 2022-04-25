from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
from apps.recipes import views

class RecipeIndexViewsTest(RecipeTestBase):
    """
    Tests if the functions are working correctly
    """
    def test_recipe_index_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
    
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        
        self.assertIs(view.func, views.category)
        
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_index_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        
        self.assertIn(
            '<h1>Não tem receitas aqui. :(</h1>',
            response.content.decode('utf-8')
        )
        
    def test_recipe_index_template_loads_recipes(self):
        """
        Check if one recipe exists
        """
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)
    
    def test_recipe_index_template_dont_load(self):
        """
        Check if recipe is published don't show
        """
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<h1>Não tem receitas aqui. :(</h1>',
            response.content.decode('utf-8')
        )