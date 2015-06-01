# -*- coding: ISO-8859-1 -*-
from datetime import date
from django.db import models

from tsm.acesso.models.usuario import Usuario
from tsm.oportunidade.models.oportunidade import Oportunidade

#Model para RTC
class Rtc(models.Model):
    criado = models.DateField(verbose_name="Criado Em", null=False, blank=False, editable=False) 
    oportunidade = models.ForeignKey(Oportunidade, verbose_name="Oportunidade", null=False, blank=False, related_name="oportunidade_rtc_set",)
    data = models.DateField(verbose_name="Data", null=False, blank=False) 
    descricao = models.TextField(verbose_name="Descrição", null=False, blank=False)
    recursos = models.ManyToManyField(
        Usuario,
        verbose_name="Recursos",
        blank=True,
        help_text="Selecione os recursos necessários para esta ação.",
        related_name="recursos_set",
    )
    hora = models.TimeField(verbose_name="Hora do Evento", null=False, blank=False, default="00:00")
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.criado = date.today()
        super(Rtc, self).save(*args, **kwargs)

    class Meta:
        app_label = "oportunidade"