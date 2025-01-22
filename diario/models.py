from django.db import models

# Create your models here.

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    fotos = models.ImageField(upload_to='fotos')

    def __str__(self):
        return self.nome
    
    class Diario(models.Model):
        titulo = models.CharField(max_length=100)
        tags = models.TextField()
        pessoas = models.ManyToManyField('Pessoa')
        texto = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        
        def __str__(self):
            return self.titulo