# -*- coding: ISO-8859-1 -*-
from datetime import date
from django.db import models

from tsm.equipe.models.membrohistorico import MembroHistorico
from django.contrib.auth.models import User

from tsm.cliente.models.carteira import Carteira

# Model de Equipes
class Membro(models.Model):
    criador = models.ForeignKey(
        User, 
        null=False, 
        verbose_name="Usuário", 
        blank=False, 
        related_name='criador',
        editable=False,
    )
    
    usuario = models.ForeignKey(
        'acesso.Usuario', 
        null=False, 
        verbose_name="Membro", 
        blank=False, 
        related_name='usuario', 
        on_delete=models.PROTECT,
        editable=False,
    )

    lider = models.ForeignKey(
        "self", 
        null=True, 
        verbose_name="Líder", 
        blank=True, 
        related_name='master',
    )

    carteiras = models.ManyToManyField(
        Carteira, 
        verbose_name='Carteiras', 
        blank=True, 
        help_text="Carteiras que um membro pode atuar. ",
        related_name="carteiras_set", 
        related_query_name="carteira"
    )

    criado = models.DateField(
        verbose_name="Criado Em", 
        null=False, 
        blank=False, 
        editable=False
    )
    
    def __unicode__(self):
        return self.usuario.first_name+' '+self.usuario.last_name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.criado = date.today()
        else:
            membroHistorico = MembroHistorico(
                nome_usuario_add=self.criador.first_name+' '+self.criador.last_name,
                nome_membro=self.usuario.first_name+' '+self.usuario.last_name,
            )

            if self.lider:
                membroHistorico.nome_lider = self.lider.usuario.first_name+' '+self.lider.usuario.last_name
                
            membroHistorico.save()
        
        super(Membro, self).save(*args, **kwargs)

    class Meta:
        app_label = 'equipe'