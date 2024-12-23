from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

        
class Feedback(models.Model):
    funcionalidades = models.TextField()
    tipo_conteudo = models.TextField()
    grupos_estudo = models.TextField()
    biblioteca_recursos = models.TextField()
    tutorias_online = models.TextField()
    integracao = models.TextField()
    funcionalidades_moveis = models.TextField()
    usabilidade = models.TextField()
    interacao = models.TextField()
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback de {self.funcionalidades[:20]}..."  # Exemplo de representação curta
