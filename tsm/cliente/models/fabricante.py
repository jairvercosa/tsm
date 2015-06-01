# -*- coding: ISO-8859-1 -*-
from django.db import models

# Model de Fabricante
class Fabricante(models.Model):
    nome = models.CharField("nome", max_length=80, null=False, blank=False)
        
    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'cliente'