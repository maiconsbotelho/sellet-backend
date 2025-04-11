from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserType(models.TextChoices):
    CLIENTE = 'cliente', 'Cliente'
    PROFISSIONAL = 'profissional', 'Profissional'
    ADMINISTRADOR = 'administrador', 'Administrador'

class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório.")
        if not username:
            raise ValueError("O username é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superusuários devem ter is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superusuários devem ter is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)

class UserProfile(AbstractUser):
    username = models.CharField(max_length=150, unique=True)  # O campo username é obrigatório
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    email = models.EmailField(unique=True)  
    first_name = models.CharField(max_length=30, blank=False, null=False)  # Nome obrigatório
    last_name = models.CharField(max_length=30, blank=False, null=False)  # Sobrenome obrigatório
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.TextField(blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    rua = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CLIENTE,
    )

    USERNAME_FIELD = 'email'  # Define o email como campo de login
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Campos obrigatórios para criar um superusuário

    objects = UserProfileManager()  # Define o gerenciador de usuários personalizado

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"