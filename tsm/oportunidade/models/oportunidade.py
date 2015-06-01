# -*- coding: ISO-8859-1 -*-
from datetime import date
from django.db import models
from django.db.models import signals

from tsm.core.models.filial import Filial
from tsm.core.models.parametro import Parametro
from tsm.core import constants

from tsm.cliente.models.cliente import Cliente

from tsm.oportunidade.signals import add_historico_oportunidade
from tsm.oportunidade.models.receita import Receita
from tsm.oportunidade.models.situacao import Situacao
from tsm.oportunidade.models.tipotemperatura import TipoTemperatura
from tsm.oportunidade.models.origem import Origem

from tsm.equipe.models.membro import Membro
from tsm.cliente.models.produto import Produto

# Model de Oportunidades
class Oportunidade(models.Model):
    filial = models.ForeignKey(Filial, verbose_name="Filial", null=False, blank=False, on_delete=models.PROTECT)
    codcrm = models.CharField("Oportunidade CRM", max_length=20, null=True, blank=True, help_text="Insira o código da oportunidade cadastrado no CRM.")
    cliente = models.ForeignKey(Cliente, verbose_name="Cliente", null=False, blank=False, on_delete=models.PROTECT)
    receita = models.ForeignKey(
        Receita, 
        verbose_name="Receita", 
        help_text="Indique qual o tipo de receita para essa oportunidade.", 
        null=False, 
        blank=False,
        on_delete=models.PROTECT,
    )
    situacao = models.ForeignKey(
        Situacao, 
        verbose_name="Situação", 
        help_text="Indique a situação da oportunidade.", 
        null=False, 
        blank=False,
        on_delete=models.PROTECT,
    )
    valor = models.FloatField(verbose_name="Valor", null=False, blank=False)
    ponderado = models.FloatField(verbose_name="Valor Ponderado", null=False, blank=True, editable=False)
    temperatura_auto = models.CharField(verbose_name="Temperatura Automática", max_length=60, null=False, blank=False)
    tipotemperatura = models.ForeignKey(
        TipoTemperatura, 
        verbose_name="Temperatura", 
        help_text="Use seu feeling e indique a temperatura que a oportunidade se encontra.", 
        null=False, 
        blank=False,
        related_name="tipotemperatura_set",
        on_delete=models.PROTECT,
    )
    responsavel = models.ForeignKey(
        'acesso.Usuario', 
        verbose_name="Executivo Responsável", 
        null=False, 
        blank=False, 
        related_name="responsavel_set",
        on_delete=models.PROTECT,
    )
    lider = models.ForeignKey(
        'acesso.Usuario', 
        verbose_name="Líder do Executivo", 
        null=False, 
        blank=False, 
        related_name="lider_oportunidade_set",
        on_delete=models.PROTECT,
    )
    criador = models.ForeignKey(
        'acesso.Usuario', 
        verbose_name="Criador", 
        null=False, 
        blank=True, 
        related_name="criado_oportunidade_set",
        on_delete=models.PROTECT,
    )
    criado = models.DateField(verbose_name="Criado Em", null=False, blank=False, editable=False)
    dtFechamento = models.DateField(verbose_name="Previsão de Fechamento", null=False, blank=False)
    obs = models.TextField("observação", null=True, blank=True, help_text="Cada observação é salva no histórico da oportunidade.")
    rtc = models.BooleanField(verbose_name='Tem RTC', help_text='Indica se a oportunidade tem RTC.',null=False, blank=False,default=False)
    dtFechado = models.DateField(verbose_name="Fechado Em", null=True, blank=True, editable=False)
    arquitetos = models.ManyToManyField(
        'acesso.Usuario',
        verbose_name="arquitetos",
        blank=True,
        help_text="Arquitetos da oportunidade que participam desta oportunidade.",
        related_name="arquitetos_set",
    )
    gpp = models.ForeignKey(
        'acesso.Usuario', 
        verbose_name="GPP", 
        null=True, 
        blank=True, 
        related_name="gpp_set",
        on_delete=models.PROTECT,
    )
    produto = models.ForeignKey(
        Produto,
        verbose_name="Produto", 
        null=True, 
        blank=False, 
        related_name="produto_oportunidade_set",
        on_delete=models.PROTECT,
    )

    mw = models.BooleanField(
        verbose_name="Must Win",
        null=False,
        blank=True,
        default=False,
    )

    bc = models.BooleanField(
        verbose_name="Best Case",
        null=False,
        blank=True,
        default=False,
    )

    origem = models.ForeignKey(
        Origem,
        verbose_name="Origem da Oportunidade",
        null=False,
        blank=False,
        related_name="origem_oportunidade_set",
        default=1,
    )
    
    def __unicode__(self):
        return self.cliente.nome + '-' + self.filial.nome + ': ' + str(self.valor)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.criado = date.today()

        perctemp = self.tipotemperatura.perc
        self.ponderado = round((self.valor * perctemp)/100,2)

        if self.tipotemperatura.tipo == 'G' and not self.dtFechado:
            self.dtFechado = date.today()
        elif self.tipotemperatura.tipo != 'G' and self.dtFechado:
            self.dtFechado = None

        super(Oportunidade, self).save(*args, **kwargs)

    class Meta:
        app_label = 'oportunidade'

signals.post_save.connect(add_historico_oportunidade, sender=Oportunidade)