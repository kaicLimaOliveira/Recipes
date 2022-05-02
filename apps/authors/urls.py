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
    path('dashboard/receita/nova-receita/', views.DashboardRecipe.as_view(), name='dashboard_new_recipe'),
    path('dashboard/receita/deletar-receita/', views.DashboardRecipe.as_view(), name='dashboard_recipe_delete'),
    path('dashboard/receita/<int:id>/editar/', views.DashboardRecipe.as_view(), name='dashboard_recipe_edit'),
    path('perfil/<int:id>/', views.ProfileView.as_view(), name='profile'),
]
