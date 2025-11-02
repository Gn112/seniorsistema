from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FormularioRegistroUsuario, FormularioVaga, FormularioPerfilCandidato
from .models import Usuario, Vaga, Application, PerfilCandidato
from django.db.models.functions import TruncMonth
from django.db.models import Count
import json


def pagina_registro(request):
    form = FormularioRegistroUsuario(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada! Por favor, faça o login.')
            return redirect('home')
        messages.error(request, 'Por favor, corrija os erros abaixo.')
    return render(request, 'candidato/registro.html', {'formulario': form})


@login_required
def dashboard_vagas(request):
    if request.user.user_type == 'empresa':
        vagas = request.user.vaga_set.all()
    else:
        vagas = Vaga.objects.all()
    return render(request, 'candidato/dashboard_vagas.html', {'vagas': vagas})


@login_required
def criar_vaga(request):
    if request.user.user_type != 'empresa':
        messages.error(request, 'Apenas empresas podem criar vagas.')
        return redirect('dashboard_vagas')
    form = FormularioVaga(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        vaga = form.save(commit=False)
        vaga.empresa = request.user
        vaga.save()
        messages.success(request, 'Vaga criada com sucesso!')
        return redirect('dashboard_vagas')
    return render(request, 'candidato/criar_vaga.html', {'formulario': form})


@login_required
def editar_perfil(request):
    if request.user.user_type != 'candidato':
        messages.error(request, 'Apenas candidatos podem editar o perfil.')
        return redirect('dashboard_vagas')
    perfil, _ = PerfilCandidato.objects.get_or_create(user=request.user)
    form = FormularioPerfilCandidato(request.POST or None, instance=perfil)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('dashboard_vagas')
    return render(request, 'candidato/editar_perfil.html', {'formulario': form})


@login_required
def editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if request.user != vaga.empresa:
        messages.error(request, 'Você não tem permissão para editar esta vaga.')
        return redirect('dashboard_vagas')
    form = FormularioVaga(request.POST or None, instance=vaga)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard_vagas')
    return render(request, 'candidato/editar_vaga.html', {'formulario': form})


@login_required
def deletar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if request.user != vaga.empresa:
        messages.error(request, 'Você não tem permissão para deletar esta vaga.')
        return redirect('dashboard_vagas')
    vaga.delete()
    return redirect('dashboard_vagas')


@login_required
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if request.user.user_type != 'candidato':
        messages.error(request, 'Apenas candidatos podem se candidatar a vagas.')
        return redirect('dashboard_vagas')

    perfil = getattr(request.user, 'perfilcandidato', None)
    if not perfil or not perfil.ultima_escolaridade or not perfil.experiencia:
        messages.error(request, 'Por favor, complete seu perfil antes de se candidatar.')
        return redirect('editar_perfil')

    _, created = Application.objects.get_or_create(candidato=request.user, vaga=vaga)
    if not created:
        messages.warning(request, 'Você já se candidatou para esta vaga.')
    return redirect('dashboard_vagas')

@login_required
def dashboard_vagas(request):
    """
    Esta é a página principal depois que o usuário fizer login.
    Mostra a lista de vagas E os gráficos (se for empresa).
    """

    usuario_logado = request.user 
    contexto = {} # Cria um dicionário vazio para os dados

    if usuario_logado.user_type == 'empresa':
        # --- Lógica da Lista de Vagas (Já existia) ---
        lista_de_vagas = usuario_logado.vaga_set.all()

        # --- LÓGICA DOS GRÁFICOS (NOVO) ---

        # Gráfico 1: Vagas criadas por Mês
        vagas_por_mes = Vaga.objects.filter(empresa=request.user) \
            .annotate(mes=TruncMonth('created_at')) \
            .values('mes') \
            .annotate(total=Count('id')) \
            .order_by('mes')

        # Prepara os dados para o JavaScript (Chart.js)
        vagas_labels = [v['mes'].strftime('%b/%Y') for v in vagas_por_mes]
        vagas_data = [v['total'] for v in vagas_por_mes]

        candidatos_por_mes = Application.objects.filter(vaga__empresa=request.user) \
            .annotate(mes=TruncMonth('created_at')) \
            .values('mes') \
            .annotate(total=Count('id')) \
            .order_by('mes')

        candidatos_labels = [c['mes'].strftime('%b/%Y') for c in candidatos_por_mes]
        candidatos_data = [c['total'] for c in candidatos_por_mes]

        contexto = {
            'vagas_labels': json.dumps(vagas_labels),
            'vagas_data': json.dumps(vagas_data),
            'candidatos_labels': json.dumps(candidatos_labels),
            'candidatos_data': json.dumps(candidatos_data),
        }

    else:
        lista_de_vagas = Vaga.objects.all()

    contexto['vagas'] = lista_de_vagas

    return render(request, 'candidato/dashboard_vagas.html', contexto)