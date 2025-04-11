from django.db import models
from django.utils import timezone
from usuarios.models import UserProfile
from servicos.models import Servico

class Agendamento(models.Model):
    cliente = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="agendamentos_cliente",
        limit_choices_to={'tipo_usuario': 'cliente'}
    )
    profissional = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="agendamentos_profissional",
        limit_choices_to={'tipo_usuario': 'profissional'}
    )
    servicos = models.ManyToManyField(Servico, related_name="agendamentos")
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=[("pendente", "Pendente"), ("confirmado", "Confirmado"), ("cancelado", "Cancelado")],
        default="pendente"
    )
    data_hora_agendamento = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.data < timezone.now().date():
            raise ValueError("A data do agendamento não pode ser no passado.")
        if self.hora < timezone.now().time() and self.data == timezone.now().date():
            raise ValueError("O horário do agendamento não pode ser no passado.")

    def __str__(self):
        return f"Agendamento de {self.cliente} com {self.profissional} em {self.data} às {self.hora}"

    class Meta:
        unique_together = ("profissional", "data", "hora")
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"