from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cep = models.CharField(max_length=8, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    rua = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    manicure = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'usuarios'


class Profissional(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField()
    imagem_url = models.URLField()
    avaliacao = models.FloatField()
    cpf = models.CharField(max_length=11, unique=True)
    quantidade_avaliacoes = models.IntegerField()
    
    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'profissionais'


class Servico(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField()
    preco = models.FloatField()
    qtde_slots = models.IntegerField()
    imagem_url = models.URLField()
    
    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'servicos'


class Agendamento(models.Model):
    data = models.DateTimeField()
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='agendamentos')
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='agendamentos')
    servicos = models.ManyToManyField(Servico, related_name='agendamentos')
    
    def __str__(self):
        return f'Agendamento de {self.usuario.nome} com {self.profissional.nome} em {self.data}'
    
    class Meta:
        db_table = 'agendamentos'
