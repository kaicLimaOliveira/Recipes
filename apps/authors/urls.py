from unicodedata import name

from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path('registro/', views.register_view, name='register' ),
    path('registro/criar/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/criar/', views.login_create, name='login_create'),
    path('sair/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/receita/nova-receita/', views.dashboard_new_recipe, name='dashboard_new_recipe'),
    path('dashboard/receita/deletar-receita/', views.dashboard_recipe_delete, name='dashboard_recipe_delete'),
    path('dashboard/receita/<int:id>/editar/', views.dashboard_recipe_edit, name='dashboard_recipe_edit'),
]
