from django.urls import path

from apps.recipes import views

# recipes:recipe
app_name = 'recipes'

urlpatterns = [
    path('', views.home, name="home"),
    path('receitas/buscar/', views.search, name="search"),
    path('receitas/categoria/<int:category_id>/', views.category, name="category"),
    path('receitas/<int:id>/', views.recipe, name="recipe"),
]
