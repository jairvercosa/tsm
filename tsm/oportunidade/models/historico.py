# -*- coding: ISO-8859-1 -*-
from datetime import date
from django.db import models

from tsm.oportunidade.models.oportunidade import Oportunidade

# Model de Oportunidades
class Historico(models.Model):
    oportunidade = models.ForeignKey(Oportunidade, verbose_name="Oportunidade", null=False, blank=False)
    criado = models.DateField(verbose_name="Criado Em", null=False, blank=False)
    nome_usuario_add = models.CharField(verbose_name="Usuário Criador", max_length=120, null=False, blank=False)
    nome_situacao = models.CharField(verbose_name="Situação", max_length=120, null=False, blank=False)
    nome_tipotemperatura = models.CharField(verbose_name="Tipo Temperatura", max_length=120, null=False, blank=False)
    nome_responsavel = models.CharField(verbose_name="Responsável", max_length=120, null=False, blank=False)
    nome_lider = models.CharField(verbose_name="Líder", max_length=120, null=False, blank=False)
    valor = models.FloatField(verbose_name="Valor", null=False, blank=False)
    ponderado = models.FloatField(verbose_name="Valor Ponderado", null=False, blank=False)
    temperatura_auto = models.CharField(verbose_name="Temperatura Automática", max_length=60, null=False, blank=False)
    dtFechamento = models.DateField(verbose_name="Fechamento", null=False, blank=False)
    obs = models.TextField("observação", null=True, blank=True, help_text="Cada observação é salva no histórico da oportunidade.")
    dtFechado = models.DateField(verbose_name="Fechado Em", null=True, blank=True)
    nome_arquitetos = models.CharField(verbose_name="Arquitetos", max_length=120, null=True, blank=True)
    nome_gpp = models.CharField(verbose_name="GPP", max_length=120, null=True, blank=True)
    nome_produto = models.CharField(verbose_name="Produto", max_length=120, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.criado = date.today()
        super(Historico, self).save(*args, **kwargs)

    class Meta:
        app_label = 'oportunidade'