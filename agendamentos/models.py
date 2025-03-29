from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from usuarios.models import UserProfile
from servicos.models import Servico

class Agendamento(models.Model):
    cliente = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='agendamentos_cliente',
        limit_choices_to={'tipo_usuario': 'cliente'}
    )
    profissional = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='agendamentos_profissional',
        limit_choices_to={'tipo_usuario': 'profissional'}
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name='agendamentos_servico'
    )
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ], default='pendente')
    data_hora_agendamento = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.data_hora_agendamento:
            self.data_hora_agendamento = timezone.make_aware(
                datetime.combine(self.data, self.hora), timezone.get_current_timezone()
            )
        super().save(*args, **kwargs)


    class Meta:
        unique_together = ('data', 'hora', 'profissional')
