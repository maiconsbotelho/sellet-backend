# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# Definindo tipos de usuário
class UserType(models.TextChoices):
    CLIENTE = 'cliente', 'Cliente'
    PROFISSIONAL = 'profissional', 'Profissional'
    ADMINISTRADOR = 'administrador', 'Administrador'

class UserProfile(AbstractUser):
    # Campos adicionais
    telefone = models.CharField(max_length=15, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CLIENTE,
    )
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username
