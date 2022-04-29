from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from apps.authors.forms.recipe_form import AuthorRecipeForm
from apps.recipes.models import Recipe

@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get_recipe(self, id=None):
        recipe = None
        
        if id is not None: 
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()
        
            if not recipe: 
                raise Http404
        
        return recipe
    
    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html', 
            context = {
                'form': form,
                'is_page_edit': False
            }
        )
        
    @method_decorator(
        login_required(login_url='authors:login', redirect_field_name='next')
    )
    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
            
        return self.render_recipe(form)    
        
    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        
        form = AuthorRecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )
        
        if form.is_valid():
            recipe = form.save(commit=False)
            
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            
            recipe.save()
            
            messages.success(request, 'Sua Receita foi salva com sucesso!')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))
            
        return self.render_recipe(form)    

@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'Deletado com sucesso')
        return redirect(reverse('authors:dashboard'))