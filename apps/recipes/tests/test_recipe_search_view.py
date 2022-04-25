from django.urls import reverse, resolve
from apps.recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeSearchViewsTest(RecipeTestBase):
    def test_recipe_search_user_correct_view_function(self):
        url = resolve(reverse('recipes:search'))
        self.assertIs(url.func, views.search)
        
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
        
    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=Teste'
        response = self.client.get(url)
        self.assertIn(
            'Pesquisa por &quot;Teste&quot;',
            response.content.decode('utf-8')
        )
        
    def test_recipe_search_can_find_recipe_by_title(self):
        title = 'This is recipe one'
        title_two = 'This is recipe two'

        recipe = self.make_recipe(
            slug='one', title=title, author_data={'username': 'one'}
        )
        
        recipe_two = self.make_recipe(
            slug='two', title=title_two, author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response = self.client.get(f'{search_url}?q={title}')
        response_two = self.client.get(f'{search_url}?q={title_two}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe, response.context['recipes'])
        self.assertNotIn(recipe_two, response.context['recipes'])

        self.assertIn(recipe_two, response_two.context['recipes'])
        self.assertNotIn(recipe, response_two.context['recipes'])

        self.assertIn(recipe, response_both.context['recipes'])
        self.assertIn(recipe_two, response_both.context['recipes'])