from django.db import models

class Departamento(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Funcionario(models.Model):

    ESCOLARIDADE_CHOICES = [
        ('fundamental', 'Ensino Fundamental'),
        ('medio', 'Ensino Médio'),
        ('tecnico', 'Técnico'),
        ('superior', 'Ensino Superior'),
        ('pos', 'Pós-graduação'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
    ]

    CONTRATO_CHOICES = [
        ('clt', 'CLT'),
        ('pj', 'PJ'),
        ('estagio', 'Estágio'),
        ('temporario', 'Temporário'),
    ]

    MODELO_TRABALHO_CHOICES = [
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
    ]

    DEPARTAMENTO_CHOICES = [
        ('ti', 'TI'),
        ('financeiro', 'Financeiro'),
        ('rh', 'Recursos Humanos'),
        ('vendas', 'Vendas'),
        ('marketing', 'Marketing'),
        ('atendimento', 'Atendimento ao Cliente'),
    ]

    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()

    data_nascimento = models.DateField()

    departamento = models.CharField(max_length=20, choices=DEPARTAMENTO_CHOICES)
    cargo = models.CharField(max_length=100)

    escolaridade = models.CharField(max_length=20, choices=ESCOLARIDADE_CHOICES)
    tipo_contrato = models.CharField(max_length=20, choices=CONTRATO_CHOICES)
    modelo_trabalho = models.CharField(max_length=20, choices=MODELO_TRABALHO_CHOICES)

    salario = models.DecimalField(max_digits=10, decimal_places=2)
    data_admissao = models.DateField()

    cidade = models.CharField(max_length=100)

    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome