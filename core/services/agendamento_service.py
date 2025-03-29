from django.utils import timezone
from datetime import datetime, timedelta
from agendamentos.models import Agendamento

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
    

@staticmethod
def pode_cancelar_agendamento(agendamento):
    """
    Verifica se o agendamento pode ser cancelado.
    O cancelamento é permitido até 24h antes do agendamento.
    """
    return agendamento.data_hora_agendamento > timezone.now() + timedelta(hours=24)


def verificar_disponibilidade(data, hora, profissional):
    """
    Verifica se o profissional já tem um agendamento no mesmo dia e horário.
    """
    return not Agendamento.objects.filter(data=data, hora=hora, profissional=profissional).exists()

from datetime import datetime

def validar_agendamento(data, hora, profissional, cliente=None):
    """
    Valida os campos data e hora do agendamento:
    - Verifica se a data e hora do agendamento são no futuro.
    - Verifica se o horário já está ocupado para o mesmo profissional.
    - Verifica se o horário já está ocupado para o cliente (caso o usuário seja cliente).
    """
    if isinstance(data, str):
        # Converte string para datetime.date
        data = datetime.strptime(data, "%Y-%m-%d").date()
    if isinstance(hora, str):
        # Converte string para datetime.time
        hora = datetime.strptime(hora, "%H:%M:%S").time()

    data_hora_agendamento = timezone.make_aware(
        datetime.combine(data, hora), timezone.get_current_timezone()
    )

    if data_hora_agendamento <= timezone.localtime():
        raise ValueError("A data e hora do agendamento devem ser no futuro.")

    if not verificar_disponibilidade(data, hora, profissional):
        raise ValueError("Esse horário já está ocupado para o profissional. Escolha outro horário.")
        
    if cliente and Agendamento.objects.filter(cliente=cliente, data_hora_agendamento=data_hora_agendamento).exists():
        raise ValueError("Esse horário já está ocupado para o cliente. Escolha outro horário.")

    return data_hora_agendamento

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
