from django.db import models

# Create your models here.
class Profissional(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField()
    imagem_url = models.URLField(null=True, blank=True)  # Torna o campo opcional

    
    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'profissionais'