from django.db import models

# Create your models here.

#Cadastros
#Vagas
#Sqls

class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    idade = models.IntegerField()
    email = models.TextField(max_length=100)
    experiencia = models.TextField(max_length=500)
    ult_escolaridade = models.CharField(max_length=1)