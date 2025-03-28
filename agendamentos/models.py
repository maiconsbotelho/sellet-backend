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
            self.data_hora_agendamento = timezone.make_aware(datetime.combine(self.data, self.hora))
        super().save(*args, **kwargs)

    @classmethod
    def pode_cancelar_agendamento(self):
        """
        Verifica se o agendamento pode ser cancelado.
        O cancelamento é permitido até 24h antes do agendamento.
        """
        return self.data_hora_agendamento - timezone.now() > timedelta(hours=24)

    @classmethod
    def verificar_disponibilidade(cls, data, hora, profissional):
        """
        Verifica se o profissional já tem um agendamento no mesmo dia e horário.
        """
        return not cls.objects.filter(data=data, hora=hora, profissional=profissional).exists()

    @classmethod
    def validar_agendamento(cls, data, hora, profissional, cliente=None):
        """
        Valida os campos data e hora do agendamento:
        - Verifica se a data e hora do agendamento são no futuro.
        - Verifica se o horário já está ocupado para o mesmo profissional.
        - Verifica se o horário já está ocupado para o cliente (caso o usuário seja cliente).
        """
        data_hora_agendamento = timezone.make_aware(datetime.combine(data, hora))

        if data_hora_agendamento <= timezone.now():
            raise ValueError("A data e hora do agendamento devem ser no futuro.")

        if not cls.verificar_disponibilidade(data, hora, profissional):
            raise ValueError("Esse horário já está ocupado para o profissional. Escolha outro horário.")
        
        if cliente and cls.objects.filter(cliente=cliente, data_hora_agendamento=data_hora_agendamento).exists():
            raise ValueError("Esse horário já está ocupado para o cliente. Escolha outro horário.")

        return data_hora_agendamento

    class Meta:
        unique_together = ('data', 'hora', 'profissional')