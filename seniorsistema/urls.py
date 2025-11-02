"""
URL configuration for seniorsistema project.
...
"""
#from django.contrib import admin
from django.urls import path
from candidato import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    #path('admin/', admin.site.urls),

    path('', 
         auth_views.LoginView.as_view(template_name='candidato/home.html'), 
         name='home'),

    path('registro/', views.pagina_registro, name='registro'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('vagas/', views.dashboard_vagas, name='dashboard_vagas'),

    path('vagas/criar/', views.criar_vaga, name='criar_vaga'),

    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    path('vagas/editar/<int:vaga_id>/', views.editar_vaga, name='editar_vaga'),

    path('vagas/deletar/<int:vaga_id>/', views.deletar_vaga, name='deletar_vaga'),

    path('vagas/candidatar/<int:vaga_id>/', views.candidatar_vaga, name='candidatar_vaga'),
]