# -*- coding: ISO-8859-1 -*-
from datetime import date
from django.db import models

from tsm.oportunidade.models.oportunidade import Oportunidade

# Model de histórico de respostas
class HistoricoResposta(models.Model):
    oportunidade = models.ForeignKey(Oportunidade, verbose_name="Oportunidade", null=False, blank=False)
    nome_usuario_add = models.CharField(verbose_name="Usuário Criador", max_length=120, null=False, blank=False)
    questao_txt = models.CharField(verbose_name="Questão", max_length=180, null=False, blank=False)
    resposta_txt = models.CharField(verbose_name="Resposta", max_length=3, null=False, blank=False)
    criado = models.DateField(verbose_name="Criado Em", null=False, blank=False, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.criado = date.today()
        super(HistoricoResposta, self).save(*args, **kwargs)

    class Meta:
        app_label = 'oportunidade'