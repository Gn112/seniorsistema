from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission 
from django.utils.translation import gettext_lazy as _

FAIXA_SALARIAL = (
    (1, 'Até 1.000'),
    (2, 'De 1.000 a 2.000'),
    (3, 'De 2.000 a 3.000'),
    (4, 'Acima de 3.000'),
)

NIVEL_ESCOLARIDADE = (
    (1, 'Ensino fundamental'),
    (2, 'Ensino médio'),
    (3, 'Tecnólogo'),
    (4, 'Ensino Superior'),
    (5, 'Pós/MBA/Mestrado'),
    (6, 'Doutorado'),
)

# Login de usuário / empregador

class Usuario(AbstractUser): 
    TIPOS_DE_USUARIO = (
        ('candidato', 'Candidato'),
        ('empresa', 'Empresa'),
    )
    
    username = None 

    email = models.EmailField(
        verbose_name='E-mail',
        max_length=100, 
        unique=True
    )
    user_type = models.CharField(
        verbose_name='Tipo de Usuário',
        max_length=10,
        choices=TIPOS_DE_USUARIO,
        default='candidato'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Remove 'username' dos campos obrigatórios

    def __str__(self):
        # Seu método __str__
        return f"{self.get_user_type_display()}: {self.email}"


class PerfilCandidato(models.Model):

    user = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'user_type': 'candidato'},
        verbose_name='Usuário'
    )
    pretensao_salarial = models.IntegerField(
        choices=FAIXA_SALARIAL,
        null=True, blank=True,
        verbose_name='Pretensão Salarial'
    )
    experiencia = models.TextField(
        verbose_name='Experiência',
        null=True, blank=True
    )
    ultima_escolaridade = models.IntegerField(
        choices=NIVEL_ESCOLARIDADE,
        null=True, blank=True,
        verbose_name='Última Escolaridade'
    )

    def __str__(self):
        return f"Perfil de {self.user.email}"


class Vaga(models.Model):

    empresa = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'empresa'},
        verbose_name='Empresa'
    )
    nome_vaga = models.CharField(
        'Nome da Vaga',
        max_length=255
    )
    faixa_salarial = models.IntegerField(
        'Faixa Salarial',
        choices=FAIXA_SALARIAL
    )
    requisitos = models.TextField('Requisitos')
    escolaridade_minima = models.IntegerField(
        'Escolaridade Mínima',
        choices=NIVEL_ESCOLARIDADE
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    def __str__(self):
        return f"{self.nome_vaga} ({self.empresa.email})"


class Application(models.Model):

    candidato = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'candidato'},
        related_name='applications',
        verbose_name='Candidato'
    )
    vaga = models.ForeignKey(
        Vaga,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Vaga'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    def __str__(self):
        return f"{self.candidato.email} -> {self.vaga.nome_vaga}"