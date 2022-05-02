import os

from django.contrib import messages
from django.db.models import Q
from django.forms import model_to_dict
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from utils.pagination import make_pagination

from apps.recipes.models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/index.html'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter( 
            is_published=True
        )
        qs = qs.select_related('author', 'category', 'author__profile')
        # qs = qs.prefetch_related('tags')
        
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'), 
            PER_PAGE
        )
        ctx.update({ 'recipes': page_obj, 'pagination_range': pagination_range })
        
        return ctx
    
class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/index.html'
    
class RecipeListViewHomeApi(RecipeListViewHome):
    template_name = 'recipes/pages/index.html'
    
    def render_to_response(self, *args, **kwargs) -> JsonResponse:
        recipes = self.get_context_data()['recipes']
        recipes_dict = list(recipes.object_list.values())
        
        return JsonResponse(
            recipes_dict,
            safe=False
        )

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs.filter(
            category_id=self.kwargs.get('category_id')
        )
        
        if not qs:
            raise Http404
        return qs

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'
    
    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        
        if not search_term:
            raise Http404
        
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) | 
                Q(description__icontains=search_term),
            ),
        )
        
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({ 
            'page_title': f'Pesquisa por "{search_term}"',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}'
        })
        
        return ctx
 
class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe.html'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs.filter(is_published=True)
        
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True
        })
        
        return ctx    
    
class RecipeDetailApi(RecipeDetail):
    def render_to_response(self, context, **response_kwargs) -> JsonResponse:
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)
        
        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['update_at'] = str(recipe.update_at)
        
        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request .build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else: 
            recipe_dict['cover'] = ''
            
        del recipe_dict['is_published']
        
        return JsonResponse(
            recipe_dict,
            safe=False
        )     
        
def theory(request, *args, **kwargs):
    recipes = Recipe.objects.all() 
    recipes = recipes.filter(title__icontains='Teste').first()
    
    context = {
        'recipes': recipes
    }
    
    return render(
        request,
        'recipes/pages/theory.html',
        context=context
    )
        
        
        
        
        