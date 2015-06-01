# -*- coding: ISO-8859-1 -*-
from django.db import models

from tsm.core.models.filial import Filial
# Model de Tipos de Meta
class TipoMeta(models.Model):
    nome = models.CharField("nome", max_length=60, null=False, blank=False)
    filial = models.ForeignKey(Filial, null=False, verbose_name="Filial", blank=False, default=1, on_delete=models.PROTECT)
    
    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'equipe'