from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_funcionarios, name='lista_funcionarios'),
    path('novo/', views.criar_funcionario, name='criar_funcionario'),
    path('editar/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('deletar/<int:id>/', views.deletar_funcionario, name='deletar_funcionario'),
    path('dashboard/', views.dashboard, name='dashboard'),
]