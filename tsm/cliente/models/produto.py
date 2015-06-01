# -*- coding: ISO-8859-1 -*-
from django.db import models

from tsm.core.models.filial import Filial
from tsm.cliente.models.fabricante import Fabricante

# Model de Produto
class Produto(models.Model):
    nome = models.CharField("nome", max_length=80, null=False, blank=False)
    fabricante = models.ForeignKey(Fabricante, verbose_name="Fabricante", blank=False, null=True)
    
    filial = models.ForeignKey(Filial, verbose_name="Unidade", blank=True, null=True, on_delete=models.PROTECT)
        
    def __unicode__(self):
        return self.nome + ' - ' + self.fabricante.nome

    class Meta:
        app_label = 'cliente'