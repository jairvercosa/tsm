# -*- coding: ISO-8859-1 -*-
from django.db import models
from tsm.core.models.filial import Filial

# Model de Tipos de Questao
class Questao(models.Model):
    ORDERS_CHOICE = (
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        (6,'6'),
        (7,'7'),
        (8,'8'),
        (9,'9'),
        (10,'10'),
    )
    ordem =  models.IntegerField(verbose_name="ordem",choices=ORDERS_CHOICE,null=False, blank=False, default=1, max_length=10)
    pergunta = models.CharField(verbose_name="pergunta", max_length=120, null=False, blank=False)
    sim = models.FloatField(verbose_name="sim", help_text="Pontuação para resposta Sim", null=False, blank=False)
    nao = models.FloatField(verbose_name="Não", help_text="Pontuação para resposta Não", null=False, blank=False)
    filial = models.ForeignKey(Filial, null=True, verbose_name="Unidade", blank=True, default=1)
    
    def __unicode__(self):
        return self.ordem

    class Meta:
        app_label = 'oportunidade'