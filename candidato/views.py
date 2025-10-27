from django.shortcuts import render
from .models import Usuario

# Create your views here.

#Funções de exibição
#- Validações
#- Cadastrar Vaga

def home(request):
    return render(request, 'candidato/home.html')

def usuario(request):
    # Salva um novo usuário no banco de dados
    novo_usuario = Usuario()
    novo_usuario.nome = request.POST.get('nome')
    novo_usuario.email = request.POST.get('email')
    novo_usuario.senha = request.POST.get('senha')
    novo_usuario.idade = request.POST.get('idade')
    novo_usuario.ult_escolaridade = request.POST.get('ult_escolaridade')
    novo_usuario.experiencia = request.POST.get('experiencia')

    novo_usuario.save()

    # Exibir a lista de usuários cadastrados
    usuarios = {
        'usuarios': Usuario.objects.all()
    }

    # Retorna os dados para a página de listagem
    return render(request, 'candidato/listagem_candidatos.html', usuarios)