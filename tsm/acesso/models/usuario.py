# -*- coding: ISO-8859-1 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager

from tsm.core.models.filial import Filial
from tsm.acesso.models.funcao import Funcao
from tsm.cliente.models.segmento import Segmento

class UsuarioReceitas(models.Model):
    usuario = models.ForeignKey('acesso.Usuario', null=True)
    receita = models.ForeignKey('oportunidade.Receita', null=True)

    class Meta:
        app_label = 'acesso'

class Usuario(User):
    """
    Model de usuários
    """
    funcao = models.ForeignKey(Funcao, null=True, verbose_name="função", help_text="Função exercida por este usuário", blank=True, on_delete=models.PROTECT)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    filiais = models.ManyToManyField(Filial, verbose_name='Filiais', 
        blank=True, help_text="Filiais que o usuário tem acesso. ",related_name="filial_set", related_query_name="filial")
    showToTeam = models.BooleanField(
        verbose_name='Exibir para equipe',
        help_text='Indica se o usuário pode ser selecionado na estrutura de uma equipe.',
        blank=False,
        default=True
    )
    assistentes = models.ManyToManyField("self", null=True, verbose_name="Assistentes", blank=True, related_name='assistentes')
    receitas = models.ManyToManyField(
        'oportunidade.Receita', 
        null=True, 
        verbose_name="Tipos de Receita", 
        blank=True, 
        related_name='usuario_receitas_set',
        help_text='Indica quais tipos de receita o usuário pode visualizar. Isso interfere na geração de metas e oportunidades, \
        onde será exibido apenas o que o usuário tem permissão. ',
        through=UsuarioReceitas
    )
    segmentos = models.ManyToManyField(
        Segmento,
        null=True, 
        verbose_name="Segmentos", 
        blank=True, 
        related_name='usuario_segmentos_set',
        help_text='Indica quais os segmentos que o usuário pode visualizar. '
    )
    forca_troca_senha = models.BooleanField(
        verbose_name="Força troca de senha no próximo logon.",
        null=False,
        blank=True,
        default=False,
    )

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        app_label = 'acesso'

    def as_dict(self):
        return {
            "id" : self.pk,
            "nome": self.first_name + ' ' + self.last_name,
            "funcao": self.funcao.nome,
            "telefone": self.telefone,
        }

    def save(self, *args, **kwargs):
        if not self.pk:
            self.forca_troca_senha = True

        super(Usuario, self).save(*args, **kwargs)

