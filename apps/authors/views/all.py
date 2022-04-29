from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.authors.forms.recipe_form import AuthorRecipeForm
from apps.recipes.models import Recipe
from apps.authors.forms import LoginForm, RegisterForm



# Create your views here.
def register_view(request) -> None:
    """Create a new view with 
    form to register a user

    Returns:
        request: None
    """
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    
    return render(request, 'authors/pages/register_view.html', { 
        'form': form,
        'form_action': reverse('authors:register_create')
    })

def register_create(request) -> None:
    """Create a new user in the database
    and show a success message   
    
    Returns:
        request: None 
    """
    if not request.POST:
        raise Http404
    
    POST = request.POST
    request.session['register_form_data'] = POST
     
    form = RegisterForm(request.POST)
    
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        form.save()
        messages.success(request, 'Seu usuário foi criado, faça login.')
        
        del request.session['register_form_data']
        return redirect(reverse('authors:login'))
    
    return redirect('authors:register')

def login_view(request) -> None:
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })

def login_create(request) -> None:
    if not request.POST:
        raise Http404()
    
    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        
        if authenticated_user is not None:
            messages.success(request, 'Você está logado!')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Credenciais inválidas')
            
        return redirect(reverse('authors:login'))
    else:
        messages.error(request, 'Usuário ou senha inválidas')
    
    return redirect(reverse('authors:dashboard'))

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        redirect(reverse('recipes:home'))
    
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('recipes:home'))
        
    logout(request)
    return redirect(reverse('recipes:home'))

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_view(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    
    return render(request, 'authors/pages/dashboard.html', 
    context={
        'recipes': recipes    
    })
