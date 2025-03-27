from django.utils import timezone
from datetime import datetime, timedelta
from agendamentos.models import Agendamento

def validar_agendamento(data, hora, profissional, cliente=None):
    """
    Valida os campos data e hora do agendamento:
    - Verifica se a data e hora do agendamento são no futuro.
    - Verifica se o horário já está ocupado para o mesmo profissional.
    - Verifica se o horário já está ocupado para o cliente (caso o usuário seja cliente).
    """
    # Combine data e hora para formar o `data_hora_agendamento`
    data_hora_agendamento = timezone.make_aware(datetime.combine(data, hora))

    # Verifica se o agendamento está no futuro
    if data_hora_agendamento <= timezone.now():
        raise ValueError("A data e hora do agendamento devem ser no futuro.")

    # Verifica se o horário já está ocupado para o mesmo profissional
    if Agendamento.objects.filter(profissional=profissional, data_hora_agendamento=data_hora_agendamento).exists():
        raise ValueError("Esse horário já está ocupado para o profissional. Escolha outro horário.")
    
    # Verifica se o horário já está ocupado para o cliente, apenas se for um cliente
    if cliente and Agendamento.objects.filter(cliente=cliente, data_hora_agendamento=data_hora_agendamento).exists():
        raise ValueError("Esse horário já está ocupado para o cliente. Escolha outro horário.")

    return data_hora_agendamento

def pode_cancelar_agendamento(agendamento: Agendamento) -> bool:
    """
    Verifica se o agendamento pode ser cancelado.
    O cancelamento é permitido até 24h antes do agendamento.
    """
    if agendamento.data_hora_agendamento - timezone.now() > timedelta(hours=24):
        return True
    return False

def associar_cliente_profissional(serializer, user, cliente_id=None, profissional_id=None):
    """
    Associa automaticamente cliente e profissional ao agendamento
    com base no tipo de usuário (cliente ou profissional).
    Administradores precisam fornecer manualmente cliente e profissional.
    """
    if user.is_superuser or user.tipo_usuario == 'administrador':
        if not cliente_id or not profissional_id:
            raise ValueError("Administrador deve fornecer cliente e profissional.")
        serializer.save(cliente_id=cliente_id, profissional_id=profissional_id)

    elif user.tipo_usuario == 'cliente':
        serializer.save(cliente=user)

    elif user.tipo_usuario == 'profissional':
        serializer.save(profissional=user)

    else:
        raise ValueError("Apenas administradores, profissionais e clientes podem criar agendamentos.")
