from django.urls import resolve, reverse
from apps.recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        """
        Check if function is execute 
        """
        view = resolve(
            reverse('recipes:recipe', args=(3,))
        )
        
        self.assertIs(view.func.view_class, views.RecipeDetail)
    
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        """
        Checks if the status code returns 404 with id not exists
        """
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1000})
        )
        
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        """
        Check if it load one page
        """
        needed_title = 'This is a detail page'
        self.make_recipe(title=needed_title)
        
        response = self.client.get(
            reverse(
                'recipes:recipe', 
                kwargs={
                    'pk': 1
                }
            )
        )
        
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)
        
    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """
        Check if recipe is published don't show
        """
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe', 
                kwargs={
                    'pk': recipe.id
                }
            )
        )

        self.assertEqual(response.status_code, 404)