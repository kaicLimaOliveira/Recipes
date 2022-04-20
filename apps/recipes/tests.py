from django.test import TestCase
from django.urls import reverse, resolve
from apps.recipes import views
from apps.recipes.models import Category, Recipe, User


class RecipeURLsTest(TestCase):
    """
    Test if the urls are correct
    """
    def test_recipe_index_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
        
    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')
        
    def test_recipe_detail_url_is_correct(self): 
        url = reverse('recipes:recipe', args=(3,))
        self.assertEqual(url, '/recipes/3/') 
        
class RecipeViewsTest(TestCase):
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
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',    
            last_name='name',    
            username='username',    
            password='123456',    
            email='username@email.com',    
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe title',
            description='Recipe description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', args=(3,))
        )
        
        self.assertIs(view.func, views.recipe )
    
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        
        self.assertEqual(response.status_code, 404)
        
        
        
        
        