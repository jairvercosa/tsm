# -*- coding: ISO-8859-1 -*-
from django.db import models
from tsm.equipe.models.snapshotequipe import SnapshotEquipe

from tsm.equipe.models.membrohistorico import MembroHistorico
from django.contrib.auth.models import User

from tsm.cliente.models.carteira import Carteira

# Model item de Snpashots de equipe
class SnapshotEquipeItem(models.Model):
    snapshot = models.ForeignKey(
        SnapshotEquipe,
        null=False,
        blank=False,
        related_name='snapshot_equipe_set',
        editable=False,
    )

    membroId = models.IntegerField(
        null=False,
        default=0,
    )

    criador = models.ForeignKey(
        User, 
        null=False, 
        verbose_name="Usuário", 
        blank=False, 
        related_name='criador_snapshot_equipe_set',
        editable=False,
    )
    
    usuario = models.ForeignKey(
        'acesso.Usuario', 
        null=False, 
        verbose_name="Membro", 
        blank=False, 
        related_name='usuario_snapshot_equipe_set', 
        on_delete=models.PROTECT,
        editable=False,
    )

    liderId = models.IntegerField(
        null=True,
    )

    carteiras = models.ManyToManyField(
        Carteira, 
        verbose_name='Carteiras', 
        blank=True, 
        help_text="Carteiras que um membro pode atuar. ",
        related_name="carteiras_snapshot_equipe_set", 
        related_query_name="carteira"
    )

    criado = models.DateField(
        verbose_name="Criado Em", 
        null=False, 
        blank=False, 
        editable=False
    )
    
    def __unicode__(self):
        return self.usuario.first_name

    class Meta:
        app_label = 'equipe'