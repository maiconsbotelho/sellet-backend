from django.db import models
from usuarios.models import UserProfile  # Importa o modelo de usuário

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    duracao = models.IntegerField(help_text="Duração do serviço em minutos")
    preco = models.DecimalField(max_digits=8, decimal_places=2)  # Preço do serviço
    profissional = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="servicos_oferecidos",
        limit_choices_to={'tipo_usuario': 'profissional'}  # Só pode ser um profissional
    )
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
