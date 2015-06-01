# -*- coding: ISO-8859-1 -*-
from django.db import models



# Model de Filiais
class Filial(models.Model):
    nome = models.CharField("nome", max_length=100, null=False, blank=False)
    matriz = models.BooleanField("É a matriz", default=False)
    responsavel = models.ForeignKey(
        'acesso.Usuario', 
        null=False, 
        blank=False,
        verbose_name="Responsável", 
        help_text="Usuário que responde pela meta da unidade. Através dessa parametrização o sistema\
        realiza os cálculos com a meta geral da unidade.",
        related_name='diretor', 
        on_delete=models.PROTECT,
        default=1,
    )
    
    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'core'

    def as_dict(self):
        return {
            "id" : self.pk,
            "nome": self.nome,
        }