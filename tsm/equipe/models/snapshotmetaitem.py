# -*- coding: ISO-8859-1 -*-
from django.db import models
from tsm.equipe.models.tipometa import TipoMeta
from tsm.equipe.models.snapshotmeta import SnapshotMeta
from tsm.oportunidade.models.receita import Receita

class SnapshotMetaItem(models.Model):
    snapshot = models.ForeignKey(SnapshotMeta, null=False,default=1)
    criador = models.ForeignKey('acesso.Usuario', null=False, verbose_name="Usuário", blank=True) #Usuario que adicionou registro 
    metaId = models.IntegerField(null=False,default=0,)
    membroId = models.IntegerField(null=False,default=0,)
    tipometa = models.ForeignKey(TipoMeta, null=False, verbose_name="Tipo da Meta", blank=False)
    receita = models.ForeignKey(Receita, null=False, verbose_name="Receita", blank=False)
    valor = models.FloatField(verbose_name="valor", null=False, blank=False)

    mesVigencia = models.CharField(verbose_name="Mês", null=False, blank=False, max_length=2,)
    anoVigencia = models.PositiveSmallIntegerField(verbose_name="Ano", null=False, blank=False, max_length=4,)
    criado = models.DateField("Criado Em", null=False, blank=False, editable=False)
    is_Visible = models.BooleanField(verbose_name="Visível para o Membro", null=False, editable=False, default=False)

    def __unicode__(self):
        return self.valor

    class Meta:
        app_label = 'equipe'