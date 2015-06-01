# -*- coding: ISO-8859-1 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from tsm.equipe.models.membrometahistorico import MembroMetaHistorico

def add_historico_membro_meta(sender, instance, signal, created, **kwargs):
    if created:
        membroMetaHistorico = MembroMetaHistorico(
            nome_usuario_add=instance.criador.first_name+' '+instance.criador.last_name,
            nome_membro=instance.membro.usuario.first_name+' '+instance.membro.usuario.last_name,
            nome_tipometa=instance.tipometa.nome,
            valor=instance.valor,
        )

        if instance.membro.lider:
            membroMetaHistorico.nome_lider = instance.membro.lider.usuario.first_name+' '+ \
                                             instance.membro.lider.usuario.last_name

        membroMetaHistorico.save()

