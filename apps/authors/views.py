from django.http import Http404
from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.contrib import messages

# Create your views here.
def register_view(request) -> None:
    """Create a new view with 
    form to register a user

    Returns:
        request: None
    """
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    
    return render(request, 'authors/pages/register_view.html', { 'form': form })

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
        form.save()
        messages.success(request, 'Seu usuário foi criado, faça login.')
        
        del request.session['register_form_data']
    
    return redirect('authors:register')