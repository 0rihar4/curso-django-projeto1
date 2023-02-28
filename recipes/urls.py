from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    # Quanto mais especifico for uma url ex = recipes/search/, mais ao topo
    # ela deve ficar e quanto menos especifico, possuir parametros
    # variaveis, mais abaixo ela deve ficar
    path('', views.home, name="home"),
    path('recipes/search/', views.search, name="search"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
    path('recipes/category/<int:category_id>/',
         views.category, name="category"),

]
