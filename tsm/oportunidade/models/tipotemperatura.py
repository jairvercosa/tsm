# -*- coding: ISO-8859-1 -*-
from django.db import models
from django.db.models import signals

from tsm.oportunidade import signals

# Model de Tipos de Temperatura
class TipoTemperatura(models.Model):
    nome = models.CharField("nome", max_length=60, null=False, blank=False)
    perc = models.FloatField(verbose_name="percentual", help_text=u"Percentual para fechar oportunidade", null=True, blank=False)
    TYPES_CHOICE = (
        ('G','Ganho'),
        ('P','Perda'),
    )
    tipo = models.CharField(verbose_name="tipo", max_length=1,choices=TYPES_CHOICE, null=True, blank=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'oportunidade'

signals.post_save.connect(signals.update_ponderado_oportunidade, sender=TipoTemperatura)