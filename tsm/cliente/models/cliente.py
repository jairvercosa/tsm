# -*- coding: ISO-8859-1 -*-
from django.db import models

from tsm.core.models.filial import Filial
from tsm.cliente.models.carteira import Carteira
from tsm.cliente.models.produto import Produto
from tsm.cliente.models.segmento import Segmento


# Model de Clientes
class Cliente(models.Model):
    nome = models.CharField("nome", max_length=120, null=False, blank=False)
    cnpj = models.CharField("CNPJ", max_length=18, null=True, blank=False)
    cnpj_matriz = models.CharField("CNPJ Matriz", help_text="Se esta empresa for uma filial, coloque aqui o CNPJ da matriz.", max_length=18, null=True, blank=True)
    endereco = models.CharField("endereço", max_length=120, null=True, blank=True)
    bairro = models.CharField("bairro", max_length=80, null=True, blank=True)
    cidade = models.CharField("cidade", max_length=80, null=True, blank=True)
    estado = models.CharField("estado", max_length=2, null=True, blank=True)
    cep = models.CharField("CEP", max_length=60, null=True, blank=True)
    webpage = models.CharField("Página Web", max_length=60, null=True, blank=True)
    criado = models.DateField("Criado Em", max_length=60, null=False, blank=False)

    filial = models.ForeignKey(Filial, null=False, verbose_name="Unidade", blank=False, on_delete=models.PROTECT)
    carteira = models.ForeignKey(Carteira, null=False, verbose_name="Carteira", help_text="Portfólio que o cliente pertence.", blank=False, on_delete=models.PROTECT)
    produtos = models.ManyToManyField(Produto, verbose_name='Produtos', 
        blank=True, help_text="Produtos que este cliente tem em sua estrutura. ",related_name="produto_set", related_query_name="produto")
    segmento = models.ForeignKey(Segmento, null=True, verbose_name="Segmento", blank=False, on_delete=models.PROTECT)
    executivo = models.ForeignKey('acesso.Usuario', null=False, verbose_name="Executivo", blank=False, on_delete=models.PROTECT, default=1)
        
    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'cliente'