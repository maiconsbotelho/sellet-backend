from django.contrib.auth.models import AbstractUser
from django.db import models

class UserType(models.TextChoices):
    CLIENTE = 'cliente', 'Cliente'
    PROFISSIONAL = 'profissional', 'Profissional'
    ADMINISTRADOR = 'administrador', 'Administrador'

class UserProfile(AbstractUser):
    # Campos adicionais
    email = models.EmailField(unique=True)  # Torne o email único
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CLIENTE,
    )
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'  # Use o email como identificador para login
    REQUIRED_FIELDS = ['username']  # Campos obrigatórios além do email

    def __str__(self):
        return self.email