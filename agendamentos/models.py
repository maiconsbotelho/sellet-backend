from django.db import models
from django.utils import timezone
from datetime import timedelta
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
    data = models.DateField()  # Campo para a data do agendamento
    hora = models.TimeField()  # Campo para a hora do agendamento
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ], default='pendente')
    
    data_hora_agendamento = models.DateTimeField()  # Campo combinado de data e hora
    
    def __str__(self):
        return f"{self.cliente} - {self.servico.nome} - {self.data} {self.hora}"

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para preencher o campo 'data_hora_agendamento' com
        base nos campos 'data' e 'hora' ao salvar.
        """
        if not self.data_hora_agendamento:
            self.data_hora_agendamento = timezone.make_aware(datetime.combine(self.data, self.hora))
        super().save(*args, **kwargs)
    
    def pode_ser_cancelado(self):
        """
        Verifica se o agendamento pode ser cancelado.
        O cancelamento é permitido até 24h antes do agendamento.
        """
        if self.data_hora_agendamento - timezone.now() > timedelta(hours=24):
            return True
        return False

    class Meta:
        unique_together = ('data', 'hora', 'profissional')
