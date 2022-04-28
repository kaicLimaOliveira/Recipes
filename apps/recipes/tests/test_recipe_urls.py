from apps.recipes import views
from django.urls import resolve, reverse

from .test_recipe_base import RecipeTestBase


class RecipeURLsTest(RecipeTestBase):
    """
    Test if the urls are correct
    """
    def test_recipe_index_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
        
    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/receitas/categoria/1/')
        
    def test_recipe_detail_url_is_correct(self): 
        url = reverse('recipes:recipe', args=(3,))
        self.assertEqual(url, '/receitas/3/') 
        
    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/receitas/buscar/')
    