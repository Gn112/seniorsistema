from django.shortcuts import render

# Create your views here.

#Funções de exibição
#- Validações
#- Cadastrar Vaga

def home(request):
    return render(request, 'candidato/home.html')

