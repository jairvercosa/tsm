# -*- coding: ISO-8859-1 -*-
from django.db import models

# Model de Tipos de Receita
class Receita(models.Model):
    nome = models.CharField("nome", max_length=60, null=False, blank=False)
    
    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'oportunidade'