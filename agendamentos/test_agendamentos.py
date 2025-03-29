import pytest
from django.utils import timezone
from datetime import datetime, timedelta
from usuarios.models import UserProfile
from agendamentos.models import Agendamento
from servicos.models import Servico
from core.services.agendamento_service import (
    associar_cliente_profissional,
    verificar_disponibilidade,
    validar_agendamento,
    pode_cancelar_agendamento
)

@pytest.fixture
def setup_data(db):
    """
    Configuração inicial para os testes.
    """
    cliente = UserProfile.objects.create_user(
        username="cliente",
        email="cliente@test.com",
        password="senha123",
        tipo_usuario="cliente"
    )
    profissional = UserProfile.objects.create_user(
        username="profissional",
        email="profissional@test.com",
        password="senha123",
        tipo_usuario="profissional"
    )
    # Cria o serviço sem profissionais inicialmente
    servico = Servico.objects.create(
        nome="Corte de Cabelo",
        descricao="Corte masculino",
        duracao=30,  # Duração em minutos
        preco=50.0
    )
    # Adiciona o profissional ao serviço
    servico.profissionais.add(profissional)

    data = timezone.now().date() + timedelta(days=1)
    hora = datetime.strptime("14:00", "%H:%M").time()
    return cliente, profissional, servico, data, hora

def test_validar_agendamento_sucesso(setup_data):
    """
    Testa se um agendamento válido é aceito.
    """
    cliente, profissional, servico, data, hora = setup_data
    data_hora = validar_agendamento(data, hora, profissional, cliente)
    assert data_hora.date() == data
    assert data_hora.time() == hora

def test_validar_agendamento_data_passada(setup_data):
    """
    Testa se um agendamento com data no passado é rejeitado.
    """
    cliente, profissional, servico, _, hora = setup_data
    data_passada = timezone.now().date() - timedelta(days=1)
    with pytest.raises(ValueError, match="A data e hora do agendamento devem ser no futuro."):
        validar_agendamento(data_passada, hora, profissional, cliente)

def test_validar_agendamento_horario_ocupado_profissional(setup_data):
    """
    Testa se um agendamento é rejeitado quando o horário já está ocupado para o profissional.
    """
    cliente, profissional, servico, data, hora = setup_data
    Agendamento.objects.create(
        cliente=cliente,
        profissional=profissional,
        servico=servico,
        data=data,
        hora=hora,
        data_hora_agendamento=validar_agendamento(data, hora, profissional, cliente)
    )
    with pytest.raises(ValueError, match="Esse horário já está ocupado para o profissional. Escolha outro horário."):
        validar_agendamento(data, hora, profissional, cliente)

def test_pode_cancelar_agendamento(setup_data):
    """
    Testa se o cancelamento é permitido até 24 horas antes do agendamento.
    """
    cliente, profissional, servico, _, _ = setup_data
    data = timezone.now().date() + timedelta(days=2)  # Agendamento no futuro
    hora = (timezone.now() + timedelta(hours=2)).time()  # Hora no futuro para evitar problemas de arredondamento

    agendamento = Agendamento(
        cliente=cliente,
        profissional=profissional,
        servico=servico,
        data=data,
        hora=hora,
        data_hora_agendamento=validar_agendamento(data, hora, profissional, cliente)
    )
    
    assert pode_cancelar_agendamento(agendamento) is True

def test_nao_pode_cancelar_agendamento(setup_data):
    """
    Testa se o cancelamento não é permitido dentro de 24 horas do agendamento.
    """
    cliente, profissional, servico, _, _ = setup_data
    data_hora_proxima = timezone.now() + timedelta(hours=23)
    agendamento = Agendamento(
        cliente=cliente,
        profissional=profissional,
        servico=servico,
        data=data_hora_proxima.date(),
        hora=data_hora_proxima.time(),
        data_hora_agendamento=data_hora_proxima
    )
    assert pode_cancelar_agendamento(agendamento) is False

def test_verificar_disponibilidade(setup_data):
    """
    Testa se a função verifica corretamente a disponibilidade do profissional.
    """
    cliente, profissional, servico, data, hora = setup_data
    assert verificar_disponibilidade(data, hora, profissional) is True
    Agendamento.objects.create(
        cliente=cliente,
        profissional=profissional,
        servico=servico,
        data=data,
        hora=hora,
        data_hora_agendamento=validar_agendamento(data, hora, profissional, cliente)
    )
    assert verificar_disponibilidade(data, hora, profissional) is False

