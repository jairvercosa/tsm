# -*- coding: ISO-8859-1 -*-
from django.db import models

from tsm.core.models.filial import Filial
from tsm.cliente.models.cliente import Cliente

# Model de Contatos
class Contato(models.Model):
    nome = models.CharField("nome", max_length=80, null=False, blank=False)
    cargo = models.CharField("cargo", max_length=80, null=False, blank=False)
    telefone = models.CharField("telefone", max_length=20, null=True, blank=True)
    celular = models.CharField("celular", max_length=20, null=True, blank=True)
    email = models.EmailField("email", max_length=100, null=True, blank=True)

    cliente = models.ForeignKey(Cliente, verbose_name="Cliente", blank=False, null=False)
    
    def __unicode__(self):
        return self.nome + ' - ' + self.cliente.nome

    class Meta:
        app_label = 'cliente'