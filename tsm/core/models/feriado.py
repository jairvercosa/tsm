# -*- coding: ISO-8859-1 -*-
from django.db import models

from tsm.core.models.filial import Filial
# Model de Feriados
class Feriado(models.Model):
    data = models.DateField(verbose_name="Data", null=False, blank=False) 
    is_repeat = models.BooleanField(
        verbose_name='Repetir Anualmente', 
        help_text='Indica se o feriado deve ser considerado todos os anos no mesmo dia e mês.',
        null=False, 
        blank=True,
        default=True
    )
    nome = models.CharField("Nome do Feriado", null=False, blank=False, max_length=60)
    filial = models.ForeignKey(
        Filial, 
        verbose_name="Filial", 
        null=True, 
        blank=True, 
        on_delete=models.PROTECT
    )

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'core'