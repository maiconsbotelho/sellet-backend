from django.db import models
from cliente.models import Cliente
from profissional.models import Profissional
from servico.models import Servico

class Agendamento(models.Model):
    PENDENTE = 'pendente'
    CONFIRMADO = 'confirmado'
    CANCELADO = 'cancelado'
    
    STATUS_CHOICES = [
        (PENDENTE, 'Pendente'),
        (CONFIRMADO, 'Confirmado'),
        (CANCELADO, 'Cancelado'),
    ]

    data = models.DateTimeField()  # Data e hora do agendamento
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='agendamentos')
    servicos = models.ManyToManyField(Servico, related_name='agendamentos')
    
    # Status do agendamento
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDENTE,
    )
    
    # Campos de auditoria
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Agendamento de {self.cliente.nome} com {self.profissional.nome} em {self.data}'
    
    class Meta:
        db_table = 'agendamentos'
        ordering = ['data']  # Para ordenar os agendamentos pela data

