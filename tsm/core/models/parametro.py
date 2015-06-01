# -*- coding: ISO-8859-1 -*-
from django.db import models

from tsm.core.models.filial import Filial
# Model de Parametros
class Parametro(models.Model):
    nome = models.CharField("nome", db_index=True, max_length=20, null=False, blank=False)
    descricao = models.CharField("descrição", max_length=255)
    valor = models.CharField("valor",max_length=50, null=False, blank=False)
    filial = models.ForeignKey(Filial, verbose_name="Filial", null=True, blank=True, default=1, on_delete=models.PROTECT)

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'core'