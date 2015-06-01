# -*- coding: ISO-8859-1 -*-
from django.db.models.signals import post_save

def add_historico_oportunidade(sender, instance, signal, created, **kwargs):
    from tsm.oportunidade.models.historico import Historico
    oportunidadeHistorico = Historico(
        oportunidade=instance,
        nome_usuario_add=instance.criador.first_name+' '+instance.criador.last_name,
        nome_situacao=instance.situacao.nome,
        nome_tipotemperatura = instance.tipotemperatura.nome,
        nome_responsavel = instance.responsavel.first_name+' '+instance.responsavel.last_name,
        nome_lider = instance.lider.first_name+' '+instance.lider.last_name,
        valor = instance.valor,
        ponderado = instance.ponderado,
        temperatura_auto = instance.temperatura_auto,
        dtFechamento = instance.dtFechamento,
        obs = instance.obs,
        dtFechado = instance.dtFechado,
    )

    if instance.arquitetos:
        arquitetos_nome = []
        for arquiteto in instance.arquitetos.all():
            arquitetos_nome.append(arquiteto.first_name)

        oportunidadeHistorico.nome_arquitetos = ', '.join(arquitetos_nome)

    if instance.gpp:
        oportunidadeHistorico.nome_gpp = instance.gpp.first_name + ' ' + instance.gpp.last_name

    if instance.produto:
        oportunidadeHistorico.nome_produto=instance.produto.nome

    oportunidadeHistorico.save()

def add_historico_resposta(sender, instance, signal, created, **kwargs):
    from tsm.oportunidade.models.historicoresposta import HistoricoResposta
    respostaHistorico = HistoricoResposta(
        oportunidade=instance.oportunidade,
        nome_usuario_add=instance.oportunidade.criador.first_name+' '+instance.oportunidade.criador.last_name,
        questao_txt=instance.questao.pergunta,
        resposta_txt='SIM' if instance.resposta else 'NAO',
    )
    respostaHistorico.save()

def update_ponderado_oportunidade(sender, instance, *args, **kwargs):
    if instance.tipo not in ['G,P']:
        oportunidades = instance.tipotemperatura_set.all()
        oportunidades = oportunidades.filter(dtFechado__isnull=True)
        for oportunidade in oportunidades:
            oportunidade.ponderado = round(oportunidade.valor * (instance.perc/100),2)
            oportunidade.save()
    