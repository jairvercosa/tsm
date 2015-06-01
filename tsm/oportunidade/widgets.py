# -*- coding: ISO-8859-1 -*-
from datetime import date, datetime, timedelta
from django.db.models import Q

from tsm.core import constants 
from tsm.core.util import getParamByName

from tsm.core.models.filial import Filial
from tsm.acesso.models.usuario import Usuario
from tsm.equipe.models.membro import Membro
from tsm.equipe.models.membrometa import MembroMeta

from tsm.equipe.models.snapshotequipe import SnapshotEquipe
from tsm.equipe.models.snapshotequipeitem import SnapshotEquipeItem
from tsm.equipe.models.snapshotmeta import SnapshotMeta
from tsm.equipe.models.snapshotmetaitem import SnapshotMetaItem

from tsm.oportunidade.models.oportunidade import Oportunidade
from tsm.oportunidade.models.tipotemperatura import TipoTemperatura
from tsm.oportunidade.models.situacao import Situacao

"""
Classe para cálculo dos widgest que aparecem no dashboard
"""
class Widgets:
    visao = None # Visão por filial, gar ou ear
    tipoMeta = None # Tipo de meta para comparação
    periodoIni = None # Data de início para buscas
    periodoFim = None # Data fim para buscas
    receitas = None # Receitas para filtro

    user = None # usuário logado
    qs = None # Resultado da query de oportunidades
    qsMeta = None # Resultado da query de metas
    qsUsuarios = None # Membros que serão pesquisados
    dictUsuariosShow = None # Usuário que serão exibidos
    isPassado = False #indica se está buscando o passado
    snapShotEquipeItem = None #guarda o snapshot da equipe no periodo pesquisado
    snapShotMetaItem = None #guarda o snapshot da meta no periodo pesquisado


    def __init__(self, user, visao, tipoMeta, periodoIni=None, periodoFim=None, receitas=None):
        """
        Inicializador da classe
        """
        self.visao = visao
        self.tipoMeta = tipoMeta
        
        hoje = datetime.today()
        if periodoIni and periodoFim:
            self.periodoIni = datetime.strptime(periodoIni,'%d/%m/%Y')
            self.periodoFim = datetime.strptime(periodoFim,'%d/%m/%Y')
            self.isPassado = True if hoje > self.periodoFim else False
        else:
            self.periodoIni = datetime.today()
            self.periodoFim = datetime.today()

        self.user = user
        self.receitas = receitas if receitas else []

    def setup(self):
        """
        Realiza as buscas necessárias para início dos cálculos
        """

        self.qsUsuarios = self.getMembros()
        self.qs = self.getOportunidades()
        self.qsMeta = self.getMetas()
        self.dictUsuariosShow = self.getDictUsuarios()

    def getMembros(self):
        """Realiza a busca de todos os membros da hierarquia
        """
        allUsers = []

        if self.isPassado:
            snpapShotEquipe = SnapshotEquipe.objects.filter(data__lte=self.periodoFim).order_by('-data')
            if not snpapShotEquipe:
                self.isPassado = False
            else:
                self.snapShotEquipeItem = SnapshotEquipeItem.objects \
                                                             .filter(
                                                                snapshot=snpapShotEquipe[0]
                                                             )
        
        # filtro por visao
        if self.visao['tipo'] == 'usuario':
            if not self.isPassado:
                membroMaster = Membro.objects.filter(usuario__id=self.visao['id'])
            else:
                membroMaster = self.snapShotEquipeItem.filter(usuario__id=self.visao['id'])
        else:
            if not self.isPassado:
                membroMaster = Membro.objects.filter(usuario__id__in=Filial.objects.filter(pk=self.visao['id']).values_list('responsavel_id'))
            else:
                membroMaster = self.snapShotEquipeItem.filter(
                                                    usuario__id__in=Filial.objects.filter(pk=self.visao['id']).values_list('responsavel_id')
                                                )

        if membroMaster:
            # busca membros
            currMember = []
            nextMembers = membroMaster

            while nextMembers:
                currMember = nextMembers
                nextMembers = []

                for item in currMember:
                    if not item.usuario.id in allUsers:
                        allUsers.append(item.usuario.id)

                    if not self.isPassado:
                        chieldMembers = Membro.objects.filter(lider=item)
                    else:
                        chieldMembers = self.snapShotEquipeItem.filter(liderId=item.membroId)

                    if chieldMembers:
                        for chield in chieldMembers:
                            nextMembers.append(chield)

        return allUsers


    def getOportunidades(self):
        """Retorna as oportunidades filtradas
        """
        qs_base_filter = []

        # filtro por visao
        if self.visao['tipo'] == 'usuario':
            qs_base_filter.append(Q(lider__id__in=self.qsUsuarios)|Q(responsavel__id__in=self.qsUsuarios))
        else:
            filialFilter = Filial.objects.get(pk=self.visao['id'])
            if not filialFilter.matriz:
                qs_base_filter.append(Q(filial__id=self.visao['id']))
        
        # filtro periodo
        qs_base_filter.append(Q(dtFechamento__gte=self.periodoIni))
        qs_base_filter.append(Q(dtFechamento__lte=self.periodoFim))

        # filtro de receitas
        qs_base_filter.append(Q(receita__id__in=self.receitas))

        # busca de oportunidades
        qsReturn = Oportunidade.objects.exclude(tipotemperatura__tipo='P')
        for filtro in qs_base_filter:
            qsReturn = qsReturn.filter(filtro)

        return qsReturn

    def getMetas(self, *args, **kwargs):
        """Retorna as metas do mês
        """
        qs_base_filter = []

        # filtra o tipo
        qs_base_filter.append(Q(tipometa__id=self.tipoMeta))

        # filtra período
        qs_base_filter.append(Q(mesVigencia__gte=self.periodoIni.strftime('%m')))
        qs_base_filter.append(Q(mesVigencia__lte=self.periodoFim.strftime('%m')))

        qs_base_filter.append(Q(anoVigencia__gte=int(self.periodoIni.strftime('%Y'))))
        qs_base_filter.append(Q(anoVigencia__lte=int(self.periodoFim.strftime('%Y'))))

        # filtra receita
        qs_base_filter.append(Q(receita__id__in=self.receitas))

        if 'usuario' in kwargs:
            # filtra um membro específico
            if not self.isPassado:
                qs_base_filter.append(Q(membro__usuario__id=kwargs['usuario']))
            else:
                usuarioSnapShot = self.snapShotEquipeItem.filter(usuario__id=kwargs['usuario']).values_list('membroId')
                qs_base_filter.append(Q(membroId__in=usuarioSnapShot))
        else:
            # filtra membro
            if self.visao['tipo'] == 'usuario':
                if not self.isPassado:
                    qs_base_filter.append(Q(membro__usuario__id=self.visao['id']))
                else:
                    usuarioSnapShot = self.snapShotEquipeItem.filter(usuario__id=self.visao['id']).values_list('membroId')
                    qs_base_filter.append(Q(membroId__in=usuarioSnapShot))
            else:
                # busca meta do responsável da unidade
                if not self.isPassado:
                    qs_base_filter.append(Q(membro__usuario__id__in=Filial.objects.filter(id=self.visao['id']).values_list('responsavel__id')))
                else:
                    usuarioSnapShot = self.snapShotEquipeItem \
                                          .filter(usuario__id__in=Filial.objects.filter(id=self.visao['id']).values_list('responsavel__id'))\
                                          .values_list('membroId')
                    qs_base_filter.append(Q(membroId__in=usuarioSnapShot))

        if not self.isPassado:
            qsMetaReturn = MembroMeta.objects.all()
        else:
            snpapShotMeta = SnapshotMeta.objects.filter(data__lte=self.periodoFim).order_by('-data')
            self.snapShotMetaItem = SnapshotMetaItem.objects\
                                        .filter(snapshot=snpapShotMeta[0])
            qsMetaReturn = self.snapShotMetaItem

        for filtro in qs_base_filter:
            qsMetaReturn = qsMetaReturn.filter(filtro)

        return qsMetaReturn

    def getDictUsuarios(self):
        """Retorna os usuário que serão exibidos na tela com suas metas e ponderados
        """
        # usuários em evidência
        if self.visao['tipo'] == 'usuario':
            usuarios = {
                self.visao['id'] : {
                    "pk": self.visao['id'],
                    "nome": Usuario.objects.get(pk=self.visao['id']).first_name,
                    "metas": self.qsMeta,
                    "ponderado": 0,
                }
            }

        else:
            usuarios = {}

            """
            Quando a visão é por filial, se busca apenas resultados dos líderes. São considerados líderes todos os
            que são liderados diretamente pelo responsável da unidade
            """
            # pega o responsável da unidade
            responsavelFilial = Filial.objects.get(id=self.visao['id']).responsavel
            if not self.isPassado:
                membros = Membro.objects.filter(lider__in=Membro.objects.filter(usuario=responsavelFilial))
            else:
                membros = self.snapShotEquipeItem.filter(
                    liderId__in=self.snapShotEquipeItem.filter(usuario=responsavelFilial).values_list('membroId')
                )

            # for para buscar ponderados de líderes
            for item in membros:
                if not item.usuario.id in usuarios:
                    usuarios.update({
                        item.usuario.id : {
                            "pk": item.usuario.id,
                            "nome": item.usuario.first_name,
                            "metas": self.getMetas(usuario=item.usuario.id),
                            "ponderado": 0,
                        }
                    })
        #print usuarios
        return usuarios

    def getTemperaturas(self):
        """
        Retorna as temperaturas parametrizadas para os gráficos
        """
        idTempParam = getParamByName(constants.PAR_TEMPGRAF,self.user.id)

        if not idTempParam:
            raise NotImplementedError("Parametro "+constants.PAR_TEMPGRAF+" não implementado") 

        strExec = '['+idTempParam+']'
        arrTemperaturas = eval(strExec)

        return arrTemperaturas


    def prospeccaoData(self):
        """
        Retorna os dados organizados de prospecção de acordo com os filtros realizados
        """

        #Usuarios que serao buscados como lideres nas oportunidades
        lideres = []

        if self.visao['tipo'] == 'usuario':
            # fator de divisão
            fator = float(getParamByName(constants.PAR_FATORCOMPENS, self.visao['id']))
            lideres.append({
                "id": self.visao['id'],
                "filhos": self.qsUsuarios,
            })
        else:
            # fator de divisão
            fator = float(getParamByName(constants.PAR_FATORCOMPENS, Filial.objects.get(id=self.visao['id']).responsavel.id))

            """se a visão é por filial então deve buscar todos os liderados dos gerentes da unidade, inclusive os que estiverem
            em níveis abaixo de 2. Ex: GAR -> LIDER CANAL -> GARES"""
            saveCurrentVisao = self.visao

            for usu in self.dictUsuariosShow:
                self.visao['tipo'] = 'usuario'
                self.visao['id'] = usu

                lideres.append({
                    "id": usu,
                    "filhos": [],
                }) 

                itens = self.getMembros()
                for item in itens:
                    lideres[len(lideres)-1]['filhos'].append(item)

            self.visao = saveCurrentVisao


        # for para buscar ponderados do líder/responsável
        for item in self.qs:
            indexUsu = 0

            matchLider = False

            for itemLider in lideres:
                if item.lider.id in itemLider['filhos']:
                    indexUsu = itemLider['id']
                    matchLider = True
                    break

            if item.responsavel.id in self.dictUsuariosShow and not matchLider:
                indexUsu = item.responsavel.id

            if indexUsu:
                self.dictUsuariosShow[indexUsu]['ponderado'] += item.ponderado


        dataReturn = {
            "data" : [],
            "labels": [],
            "values": [],
            "table_data" : [],
            "ok": True,
        }

        # atribui valores
        for idx in self.dictUsuariosShow:
            usuario = self.dictUsuariosShow[idx]
            if usuario['metas']:
                # percentual em relação a 2x a meta 
                meta = usuario['metas'][0].valor
                percent = [100,50,int((usuario['ponderado']/(meta*2))*100)]
                desencaixe = (meta*2) - usuario['ponderado']
            else:
                percent = [0,0,100]
                meta = 0
                desencaixe = 0

            dataReturn['data'].append(percent)
            dataReturn['labels'].append(usuario['nome'])
            
            dataReturn['values'].append(meta*2) # 2x a meta
            dataReturn['values'].append(meta) # meta
            dataReturn['values'].append(usuario['ponderado']) # ponderado
            fatorx = 0

            if meta:
                fatorx = round(usuario['ponderado']/meta,2)
                if fatorx < 1:
                    dataReturn['ok'] = False

            dataReturn['table_data'].append({
                "title": usuario['nome'],
                "ponderado": usuario['ponderado'],
                "desencaixe": round(desencaixe,2),
                "compensacao": round(desencaixe/fator if fator else 0,2),
                "fatorx": fatorx,
            })

        return dataReturn

    def heatData(self):
        """
        Dados para o gráfico de heat
        """

        # busca os tipos de temperatura para o label
        idTemperaturas = self.getTemperaturas()
        tipos = []
        for idTemp in idTemperaturas:
            qsTemperaturas = TipoTemperatura.objects.filter(id__in=idTemp)
            
            itens = ''
            for item in qsTemperaturas:
                if itens:
                    itens = itens+'+'+item.nome
                else:
                    itens = item.nome

            tipos.append(itens)

        tipos.append('Fator X Real')

        data = {
            "data":[],
            "tipos": tipos,
        }

        # monta o array de dados para guardar o valor depois
        for idx in self.dictUsuariosShow:
            usuario = self.dictUsuariosShow[idx]

            if usuario['metas']:
                meta = usuario['metas'][0].valor
            else:
                meta = 0

            # monta dados pra temperaturas
            temperaturas = []
            for item in idTemperaturas:
                temperaturas.append({
                    "ids": item,
                    "valor": 0,
                })

            data['data'].append({
                "id": usuario["pk"],
                "nome": usuario["nome"],
                "fatorx": 0.00,
                "grafico": [meta],
                "table_data": [],
                "temperaturas": temperaturas,
                "totalPonderado": 0,
            })


        # monta o valor com as oportunidades
        for item in self.qs:
            
            # encontra usuário
            for idx, usuario in enumerate(data['data']):
                if usuario['id'] == item.lider.id or usuario['id'] == item.responsavel.id:

                    # encontra tipo de temperatura
                    for idxTemp, temperatura in enumerate(data['data'][idx]['temperaturas']):
                        if item.tipotemperatura.id in temperatura['ids']:
                            data['data'][idx]['temperaturas'][idxTemp]['valor'] += item.ponderado
                            data['data'][idx]['totalPonderado'] += item.ponderado


        # atribui valores restantes
        for idx, item in enumerate(data['data']):
            # atualiza dados para o grafico
            if data['data'][idx]['grafico'][0]:
                data['data'][idx]['fatorx'] = round(item['totalPonderado']/data['data'][idx]['grafico'][0],2)
            else:
                data['data'][idx]['fatorx'] = 0
                
            data['data'][idx]['grafico'].append(item['totalPonderado'])

            for idxTemp, temp in enumerate(item['temperaturas']):
                if item['totalPonderado']:
                    percentualVal = int((temp['valor']/item['totalPonderado'])*100)
                    if percentualVal > 100:
                        percentualVal = 100
                else:
                    percentualVal = 0

                if idxTemp==0:
                    percentual = 'G'+str(percentualVal) if percentualVal >= 80 else 'R'+str(percentualVal)
                elif idxTemp==1:
                    percentual = 'G'+str(percentualVal) if percentualVal <= 15 else 'R'+str(percentualVal)
                else:
                    percentual = 'G'+str(percentualVal) if percentualVal <= 5 else 'R'+str(percentualVal)

                data['data'][idx]['table_data'].append(percentual)

        return data

    def heatGross(self):
        """Retorno dos dados para fcst gross
        """

        # busca os tipos de temperatura para o label
        idTemperaturas = self.getTemperaturas()
        tipos = []
        for idTemp in idTemperaturas:
            qsTemperaturas = TipoTemperatura.objects.filter(id__in=idTemp)
            
            itens = ''
            for item in qsTemperaturas:
                if itens:
                    itens = itens+'+'+item.nome
                else:
                    itens = item.nome

            tipos.append(itens)

        total=0
        fechado=0

        # monta dados pra temperaturas
        temperaturas = []
        for item in idTemperaturas:
            temperaturas.append({
                "ids": item,
                "valor": 0,
            })

        # monta o valor com as oportunidades
        for item in self.qs:
            total += item.valor

            if item.dtFechado:
                fechado += item.valor

            # encontra tipo de temperatura
            for idxTemp, temperatura in enumerate(temperaturas):
                if item.tipotemperatura.id in temperatura['ids']:
                    temperaturas[idxTemp]['valor'] += item.valor

        data = {
            "total": total,
            "tipos":tipos,
            "fechado":fechado,
            "data":[],
            "values":[],
            "meta":[],
            "ok":True,
        }

        # atribui valores restantes
        for idxTemp, temp in enumerate(temperaturas):
            data['values'].append(temp['valor'])

            if total:
                if total-fechado:
                    percentual = round((temp['valor']/(total-fechado))*100)
                else:
                    percentual = 0
            else:
                percentual = 0

            data['data'].append(percentual)

            if idxTemp==0:
                meta = 80
                if percentual < meta:
                    data['ok'] = False
            elif idxTemp==1:
                meta = 15
                if percentual > meta:
                    data['ok'] = False
            else:
                if percentual > meta:
                    data['ok'] = False
                meta = 5

            percentMeta = meta-percentual if meta-percentual>=0 else 0
            

            data['meta'].append([percentMeta,percentual])

        return data
    
    def linearidadeData(self):
        """Retorna os dados para o gráfico de linearidade
        """
        usuarios = self.dictUsuariosShow
        data = []
        diasStr = '['+getParamByName(constants.PAR_DIASLINEARIDADE,self.user.id)+']'
        
        if not diasStr:
            raise NotImplementedError("Parametro "+constants.PAR_DIASLINEARIDADE+" não implementado") 

        dias = eval(diasStr)

        if self.periodoIni > self.periodoFim:
            raise NotImplementedError("Data de fim da pesquisa não pode ser menor que a data de início.")

        diferencaDias = self.periodoFim - self.periodoIni

        # monta usuários que irão aparecer
        for obj in usuarios:
            usuario = usuarios[obj]

            meta = usuario['metas'][0].valor if usuario['metas'] else 0
            item = {
                "id": usuario['pk'],
                "nome": usuario["nome"],
                "items": [],
                "metaReal": meta,
                "filhos": [],
            }

            """se a visão é por filial então deve buscar todos os liderados dos gerentes da unidade, inclusive os que estiverem
            em níveis abaixo de 2. Ex: GAR -> LIDER CANAL -> GARES"""
            saveCurrentVisao = self.visao

            self.visao['tipo'] = 'usuario'
            self.visao['id'] = usuario['pk']

            item['filhos']=self.getMembros()
            self.visao = saveCurrentVisao


            # monta os valores para os dias
            for dia in dias:

                # testa se é um número
                if meta:
                    metaPercent = int(dia[1])
                    if dia[2] == '>':
                        metaItem = round(meta,2)
                    else:
                        metaItem = round(meta*(metaPercent*0.01),2)
                else:
                    metaItem = 0

                percentDia = int(dia[0])
                diasSoma = int(diferencaDias.days*(percentDia*0.01)) + 1
                diaData = self.periodoIni+ timedelta(days=diasSoma)

                item['items'].append({
                    "dia": date(diaData.year,diaData.month,diaData.day),
                    "percentmeta": dia[1],
                    "indicador": dia[2],
                    "meta": metaItem,
                    "ponderado": 0,
                    "percTotal": 0,
                })

            data.append(item)

        # atribui os valores
        for item in self.qs:
            # encontra usuário
            for idx, itemData in enumerate(data):
                if item.lider.id in itemData['filhos'] or itemData['id'] == item.responsavel.id:
                    #if itemData['id'] in [item.lider.id, item.responsavel.id]:
                    # monta os valores para os dias
                    for x, dia in enumerate(itemData['items']):
                        if item.dtFechado:
                            if item.dtFechado <= dia['dia']:
                                data[idx]['items'][x]['ponderado'] += item.valor
                        elif item.dtFechamento <= dia['dia']:
                            data[idx]['items'][x]['ponderado'] += round(item.valor * (item.situacao.perc/100),2)

        # atribui percentual
        for x, item in enumerate(data):
            for y, itemY in enumerate(item['items']):
                if item['metaReal']:
                    data[x]['items'][y]['percTotal'] = round((itemY['ponderado']/item['metaReal'])*100,2)
                else:
                    data[x]['items'][y]['percTotal'] = 100

                # converte dia para string para serialização do JSON
                data[x]['items'][y]['dia'] = data[x]['items'][y]['dia'].strftime('%d/%m/%Y')

        return data

    def entregaData(self):
        """Retorna os dados para o gráfico de entrega
        """
        qsSituacao = Situacao.objects.all()
        usuarios = []

        # Monta legenda
        legenda = []
        for situacao in qsSituacao:
            legenda.append(situacao.nome)
            texto = 'Md. '
            texto = texto + situacao.nome.encode('ISO-8859-1')
            legenda.append(texto)

        
        # monta os dados para cada usuario
        for itemUsu in self.dictUsuariosShow:
            usuario = self.dictUsuariosShow[itemUsu]

            itemAdd = {
                "id": usuario['pk'],
                "nome": usuario['nome'],
                "metas": usuario['metas'],
                "itemsSituacao": [],
                "realizado":0,
                "corrigida":0,
                "medicao":0,
                "percent":0,
                "filhos": [],
            }

            """se a visão é por filial então deve buscar todos os liderados dos gerentes da unidade, inclusive os que estiverem
            em níveis abaixo de 2. Ex: GAR -> LIDER CANAL -> GARES"""
            saveCurrentVisao = self.visao

            self.visao['tipo'] = 'usuario'
            self.visao['id'] = usuario['pk']

            itemAdd['filhos'] = self.getMembros()
            self.visao = saveCurrentVisao

            for situacao in qsSituacao:
                itemAdd['itemsSituacao'].append({
                    "id": situacao.id,
                    "nome": '',
                    "meta": 0,
                    "valor": 0,
                    "ponderado": 0,
                    "qtd": 0,
                    "fator": situacao.fator,
                    "operador": situacao.operador, 
                })

            usuarios.append(itemAdd)
            

        # monta os dados com as oportunidades
        for oportunidade in self.qs:

            # procura usuário
            for idx, usuario in enumerate(usuarios):
                #if usuario['id'] in [oportunidade.lider.id, oportunidade.responsavel.id]:
                if oportunidade.lider.id in usuario['filhos'] or usuario['id'] == oportunidade.responsavel.id:

                    # verifica se está fechado
                    if oportunidade.dtFechado:
                        usuarios[idx]['realizado'] += oportunidade.valor

                    # atualiza dados da situação
                    for idxSituacao, situacao in enumerate(usuario['itemsSituacao']):
                        if situacao['id'] == oportunidade.situacao.id:
                            usuarios[idx]['itemsSituacao'][idxSituacao]['nome'] = oportunidade.situacao.nome
                            usuarios[idx]['itemsSituacao'][idxSituacao]['valor'] += oportunidade.valor
                            usuarios[idx]['itemsSituacao'][idxSituacao]['ponderado'] += 0 if oportunidade.dtFechado else round(oportunidade.valor * (oportunidade.situacao.perc * 0.01),2)
                            usuarios[idx]['itemsSituacao'][idxSituacao]['qtd'] += 1
                            usuarios[idx]['medicao'] += 0 if oportunidade.dtFechado else round(oportunidade.valor * (oportunidade.situacao.perc * 0.01),2)

        # atribui metas
        for idx, usuario in enumerate(usuarios):
            #corrige a meta retirando o que já foi fechado
            if usuario['metas']:
                corrigido = (usuario['metas'][0].valor - usuario['realizado'])
            else:
                corrigido = 0

            usuarios[idx]['corrigida'] = corrigido
            #faz o cálculo das metas considerando o valor corrigido
            for idxSituacao, situacao in enumerate(usuario['itemsSituacao']):
                if usuario['metas']:
                    if situacao['operador'] == 'D':
                        meta = round(corrigido/situacao['fator'],2)
                    else:
                        meta = round(corrigido*situacao['fator'],2)

                    usuarios[idx]['itemsSituacao'][idxSituacao]['meta'] = meta


        # finaliza enviando os dados da maneira esperada pelo frontend
        data = {
            "data": [],
            "labels": [],
            "values": [],
            "table_data": [],
            "legenda": legenda,
            "fatorpond": float(getParamByName(constants.PAR_POND66, self.user.id)),
            "ok": True,
        }

        for usuario in usuarios:
            situacaoData = []
            for situacao in usuario['itemsSituacao']:
                situacaoData.append(situacao['meta'])
                situacaoData.append(situacao['ponderado'])

                data['values'].append(situacao['meta'])
                data['values'].append(situacao['ponderado']) #Valor ponderado que é exibido no gráfico.

                if(situacao['meta'] > situacao['ponderado']):
                    data['ok'] = False

            data['data'].append(situacaoData)

            percent = 100
            meta = 0
            if usuario['corrigida']:
                usuario['metas'][0].valor
                if usuario['metas']:
                    percent = round((usuario['realizado']/usuario['metas'][0].valor)*100,2)
                    meta = usuario['metas'][0].valor

            data['labels'].append(usuario['nome'])
            data['table_data'].append({
                "itemsSituacao": usuario['itemsSituacao'], #Dados sobre as situações
                "title": usuario['nome'], #Nome do usuário
                "realizado": usuario['realizado'], #Valor total fechado
                "corrigida": usuario['corrigida'], #Meta - valor fechado = meta corrigida
                "medicao": usuario['medicao'], #Somatório do valor total ponderado de pedra + upside
                "meta": meta, #Meta cheia
                "percent": percent, #Percentual de atingimento da meta (meta X Fechado)
                "valFatorPond": round(usuario['medicao'] * data['fatorpond'],2), #Coluna 0.66
            })

        return data