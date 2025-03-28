from django.utils import timezone
from datetime import datetime, timedelta

def associar_cliente_profissional(serializer, user, cliente_id=None, profissional_id=None):
    """
    Associa automaticamente cliente e profissional ao agendamento
    com base no tipo de usuário (cliente ou profissional).
    Administradores precisam fornecer manualmente cliente e profissional.
    """
    if user.is_superuser or user.tipo_usuario == 'administrador':
        if not cliente_id or not profissional_id:
            raise ValueError("Administradores devem fornecer cliente e profissional.")
        serializer.save(cliente_id=cliente_id, profissional_id=profissional_id)

    elif user.tipo_usuario == 'cliente':
        if not profissional_id:
            raise ValueError("Clientes devem fornecer o profissional.")
        serializer.save(cliente=user, profissional_id=profissional_id)

    elif user.tipo_usuario == 'profissional':
        serializer.save(profissional=user)

    else:
        raise ValueError("Apenas administradores, profissionais e clientes podem criar agendamentos.")

def calcular_data_hora_agendamento(data, hora):
    """
    Calcula o campo 'data_hora_agendamento' com base nos campos 'data' e 'hora'.
    """
    return timezone.make_aware(datetime.combine(data, hora))

def obter_intervalo_hoje():
    """
    Retorna o intervalo de hoje (início e fim do dia).
    """
    today = timezone.now().date()
    return today, today

def obter_intervalo_ontem():
    """
    Retorna o intervalo de ontem (início e fim do dia).
    """
    yesterday = timezone.now().date() - timedelta(days=1)
    return yesterday, yesterday

def obter_intervalo_semana_atual():
    """
    Retorna o intervalo da semana atual (segunda-feira até domingo).
    """
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Segunda-feira
    end_of_week = start_of_week + timedelta(days=6)  # Domingo
    return start_of_week, end_of_week

def obter_intervalo_mes_atual():
    """
    Retorna o intervalo do mês atual (primeiro dia até o último dia do mês).
    """
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    next_month = today.replace(day=28) + timedelta(days=4)  # Garante o próximo mês
    end_of_month = next_month - timedelta(days=next_month.day)
    return start_of_month, end_of_month