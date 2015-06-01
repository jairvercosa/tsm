# -*- coding: ISO-8859-1 -*-
from datetime import date
from django.db import models

# Model de Membro Meta Historico
class MembroMetaHistorico(models.Model):
    nome_usuario_add = models.CharField("Usuário Criador", max_length=120, null=False, blank=False)
    nome_membro = models.CharField("Membro", max_length=120, null=False, blank=False)
    nome_lider = models.CharField("Líder", max_length=120, null=False, blank=False)
    nome_tipometa = models.CharField("Tipo de Meta", max_length=60, null=False, blank=False)

    valor = models.FloatField(verbose_name="valor", null=False, blank=False)
    
    criado = models.DateField(verbose_name="Criado Em", null=False, blank=False)
    
    def __unicode__(self):
        return self.nome_usuario_add

    def save(self, *args, **kwargs):
        if not self.pk:
            self.criado = date.today()
        super(MembroMetaHistorico, self).save(*args, **kwargs)

    class Meta:
        app_label = 'equipe'
