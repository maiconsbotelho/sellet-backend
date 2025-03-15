from django.db import models # type: ignore

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    senha = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'clientes'