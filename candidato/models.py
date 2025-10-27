from django.db import models

# Create your models here.

#Cadastros
#Vagas
#Sqls

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    idade = models.IntegerField()
    email = models.CharField(max_length=100)
    experiencia = models.CharField(max_length=500)
    ult_escolaridade = models.CharField(max_length=1)