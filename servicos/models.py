from django.db import models
from usuarios.models import UserProfile  # Importa o modelo de usuário

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    duracao = models.IntegerField(help_text="Duração do serviço em minutos")
    preco = models.DecimalField(max_digits=8, decimal_places=2)  # Preço do serviço
    profissionais = models.ManyToManyField(
        UserProfile,
        related_name="servicos_oferecidos",
        limit_choices_to={'tipo_usuario': 'profissional'},  # Apenas profissionais podem ser vinculados
        blank=True  # Permite que o serviço seja criado sem profissionais inicialmente
    )
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'