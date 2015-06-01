# -*- coding: ISO-8859-1 -*-
from datetime import date
from django.db import models
from django.db.models import signals

from tsm.equipe.signals import add_historico_membro_meta
from tsm.equipe.models.tipometa import TipoMeta
from tsm.equipe.models.membro import Membro

from tsm.cliente.models.carteira import Carteira
from tsm.oportunidade.models.receita import Receita

# Model de Metas de Membros de Equipe
class MembroMeta(models.Model):

    def validate_anoVigencia(value):
        from django.core.exceptions import ValidationError
        """
        Verifica se é um ano válido
        """
        if value < 2000:
            raise ValidationError('%s é um ano inválido' % value)

    criador = models.ForeignKey('acesso.Usuario', null=False, verbose_name="Usuário", blank=True) #Usuario que adicionou registro 
    membro = models.ForeignKey(Membro, null=False, verbose_name="Membro", blank=False)
    tipometa = models.ForeignKey(TipoMeta, null=False, verbose_name="Tipo da Meta", blank=False)
    receita = models.ForeignKey(Receita, null=False, verbose_name="Receita", blank=False, default=1)
    valor = models.FloatField(verbose_name="valor", null=False, blank=False)

    MONTH_CHOICE = (
        ('01','Janeiro'),
        ('02','Fevereiro'),
        ('03','Março'),
        ('04','Abril'),
        ('05','Maio'),
        ('06','Junho'),
        ('07','Julho'),
        ('08','Agosto'),
        ('09','Setembro'),
        ('10','Outubro'),
        ('11','Novembro'),
        ('12','Dezembro'),
    )
    mesVigencia = models.CharField(verbose_name="Mês", null=False, blank=False, max_length=2, choices=MONTH_CHOICE, default=str(date.today().month).zfill(2))
    anoVigencia = models.PositiveSmallIntegerField(verbose_name="Ano", null=False, blank=False, max_length=4, validators=[validate_anoVigencia])
    criado = models.DateField("Criado Em", null=False, blank=False, editable=False)
    is_Visible = models.BooleanField(verbose_name="Visível para o Membro", null=False, editable=False, default=False)
    
    def __unicode__(self):
        return str(self.valor) + '-' + self.membro.usuario.first_name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.criado = date.today()
        super(MembroMeta, self).save(*args, **kwargs)

    class Meta:
        app_label = 'equipe'
        unique_together=(('membro','tipometa','receita','mesVigencia','anoVigencia'),)

signals.post_save.connect(add_historico_membro_meta, sender=MembroMeta)