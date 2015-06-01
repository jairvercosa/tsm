# -*- coding: ISO-8859-1 -*-
from django.db import models

# Model de Situação
class Situacao(models.Model):
    nome = models.CharField("nome", max_length=60, null=False, blank=False)
    perc = models.FloatField("percentual", null=False, blank=False, default=0)
    fator = models.FloatField(
        verbose_name="fator", 
        null=False, 
        blank=False, 
        default=0,
        help_text="Este fator defini o valor que será exibido nos gráficos relacionados a situação das oportunidades.",
    )
    TYPES_CHOICE = (
        ('D','Divisor'),
        ('M','Multiplicador'),
    )
    operador = models.CharField(
        verbose_name="operador", 
        max_length=1,
        choices=TYPES_CHOICE, 
        null=False, 
        blank=False,
        default='M',
        help_text="Indica qual operação será realizada com o fator.",
    )
    
    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'oportunidade'