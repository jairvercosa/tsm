# -*- coding: ISO-8859-1 -*-
from datetime import date
from django.db import models
from django.db.models import signals

from tsm.oportunidade.signals import add_historico_resposta
from tsm.oportunidade.models.oportunidade import Oportunidade
from tsm.oportunidade.models.questao import Questao

#Model de respostas das perguntas
class Resposta(models.Model):
    questao = models.ForeignKey(Questao, verbose_name="Questão", null=False, blank=False, on_delete=models.PROTECT)
    oportunidade = models.ForeignKey(Oportunidade, verbose_name="Oportunidade", null=False, blank=False)
    resposta = models.BooleanField(verbose_name="Oportunidade", null=False, blank=False)
    criado = models.DateField(verbose_name="Criado Em", null=False, blank=False, editable=False) 

    def save(self, *args, **kwargs):
        if not self.pk:
            self.criado = date.today()
        super(Resposta, self).save(*args, **kwargs)

    class Meta:
        app_label = "oportunidade"

signals.post_save.connect(add_historico_resposta, sender=Resposta)