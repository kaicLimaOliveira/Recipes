from unittest import skip

from django.forms import ValidationError
from django.test import TestCase
from django.urls import resolve, reverse

from apps.recipes import views
from apps.recipes.models import Category, Recipe, User

# assertEqual - verifica se a quantidade passada é igual a recebida, usando o context func da view
# assertIn - verifica se o conteudo esta dentro do conteudo Html

class RecipeTestBase(TestCase):
    def setUp(self) -> None:        
        return super().setUp()
    
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)
    
    def make_author(
        self,
        first_name='user',    
        last_name='name',    
        username='username',    
        password='123456',    
        email='username@email.com'
    ):
        
        return User.objects.create_user(
            first_name=first_name,    
            last_name=last_name,    
            username=username,    
            password=password,     
            email=email,     
        )
        
    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Title',
        description='Recipe Description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutos',
        servings=5,
        servings_unit='Porções',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
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

class RecipeURLsTest(RecipeTestBase):
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
        
class RecipeViewsTest(RecipeTestBase):
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
        
    def test_recipe_detail_view_function_is_correct(self):
        """
        Check if function is execute 
        """
        view = resolve(
            reverse('recipes:recipe', args=(3,))
        )
        
        self.assertIs(view.func, views.recipe)
    
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        """
        Checks if the status code returns 404 with id not exists
        """
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
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
                    'id': 1
                }
            )
        )
        
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)
        
    def test_recipe_detail_template_dont_load(self):
        """
        Check if recipe is published don't show
        """
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe', 
                kwargs={
                    'id': recipe.id
                }
            )
        )

        self.assertEqual(response.status_code, 404)
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        
        self.assertIs(view.func, views.category)
        
    def test_recipe_category_template_loads_recipes(self):
        """
        Check if one recipe exists
        """
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        
        self.assertIn(needed_title, content)
        
    def test_recipe_category_template_dont_load(self):
        """
        Check if recipe is published don't show
        """
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe', 
                kwargs={'id': recipe.category.id}
            )
        )

        self.assertEqual(response.status_code, 404)
        
class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def test_recipe_title_max_length(self):
        """
        Check eaises error if title has more than 65 chars
        """
        self.recipe.title = 'A' * 70
        
        with self.assertRaises(ValidationError):
            self.recipe.full_clean() # validation to model
            # self.recipe.save()
        
