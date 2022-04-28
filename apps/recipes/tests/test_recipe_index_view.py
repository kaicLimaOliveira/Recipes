from unittest.mock import patch

from apps.recipes import views
from django.urls import resolve, reverse

from .test_recipe_base import RecipeTestBase


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
        
    @patch('apps.recipes.views.PER_PAGE', new=5)
    def test_recipe_index_is_paginated(self):
        """
        Check how many recipes per page exist
        """
        for i in range(20):
            kwargs = { 'author_data': { 'username': f'u{i}'} , 'slug': f'r{i}',  }
            self.make_recipe(**kwargs)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator
        
        self.assertEqual(paginator.num_pages, 4)
    
    def test_invalid_page_query_uses_page_one(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=12A')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
