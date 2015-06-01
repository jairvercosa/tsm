if not self.request.user.has_perm('oportunidade.list_all_opportunities'):
            membros = Membro.objects.filter(usuario__id=request.user.id)
            if membros.exists():
                membro = membros[0]
                children = Membro.objects.filter(lider__id=membro.id)
                qs_base_filter = Q(responsavel__id=membro.usuario.id) | Q(lider__id=membro.usuario.id)
                
                if children:
                    while children:
                        for item in children:
                            qs_base_filter = qs_base_filter | Q(lider__id=item.usuario.id)

                        children = Membro.objects.filter(
                            lider__id__in = children.values_list('id', flat=True)
                        )
        else:
            qs_base_filter = Q(
                filial__id__in=Usuario.objects \
                                      .filter(id=request.user.id) \
                                      .values_list('filiais__id', flat=True)
            )

        oportunidades = Oportunidade.objects.filter(qs_base_filter)
        oportunidades.exclude(dtFechamento__lt=date(date.today().year, date.today().month, 1)) \
                     .exclude(tipotemperatura__tipo='P')

        #FCST Gross
        temperaturas = [
            [1,6], #Adiada + Alta
            [2], #Media
            [3], #Fechada 
        ]
        totalGross = float(0)
        gross = []
        for item in temperaturas:
            temps = TipoTemperatura.objects.filter(id__in=item)
            strTitle = ''
            for temp in temps:
                if strTitle:
                    strTitle = strTitle + ' + '
                strTitle = strTitle + temp.nome

            gross.append({
                'id': item,
                'title': strTitle,
                'value': 0,
            })

        #lideres
        lideres = []
        for oportunidade in oportunidades:
            if not oportunidade.lider.id in lideres:
                lideres.append(oportunidade.lider.id);

        #FCST Ponderado
        totalPonderado = float(0)
        ponderado = []
        for item in lideres:
            ponderado.append({
                'id': item,
                'name': '',
                'value':0,
            })

        #FATOR Situacao (P/U)
        totalSituacao = 0
        situacoes = Situacao.objects.all()
        fatorSit = []
        for item in lideres:
            fatorSit.append({
                'id': item,
                'name': '',
                'situacoes':[],
            })

            for situacao in situacoes:
                fatorSit[len(fatorSit)-1]['situacoes'].append({
                    'id': situacao.id,
                    'name': situacao.nome,
                    'perc': situacao.perc,
                    'value': 0,
                })

        #FATOR Calculo (66)
        totalFator = float(0)
        fatorCal = []
        for item in lideres:
            fatorCal.append({
                'id': item,
                'name': '',
                'value': 0,
            })

        #Realiza calculo
        fatorX = []
        for oportunidade in oportunidades:
            #atualiza dados do Gross
            totalGross += oportunidade.valor
            i = 0
            for item in gross:
                if oportunidade.tipotemperatura.id in item['id']:
                    gross[i]['value'] += oportunidade.valor
                i += 1

            #atualiza dados do ponderado
            totalPonderado += oportunidade.ponderado
            i = 0
            for item in ponderado:
                if oportunidade.lider.id == item['id']:
                    ponderado[i]['value'] += oportunidade.ponderado
                    ponderado[i]['name'] = oportunidade.lider.first_name
                i += 1

            #atualiza dados do fator situacao
            totalSituacao += round((oportunidade.valor * oportunidade.situacao.perc)/100,2)
            i = 0
            for item in fatorSit:
                if oportunidade.lider.id == item['id']:
                    fatorSit[i]['name'] = oportunidade.lider.first_name
                    fatorX.append({
                        "name": fatorSit[i]['name'],
                        "value": 0,
                    })

                    j = 0
                    for situacao in item['situacoes']:
                        if situacao['id'] == oportunidade.situacao.id:
                            fatorSit[i]['situacoes'][j]['value'] = round((oportunidade.valor * oportunidade.situacao.perc)/100,2)
                            fatorX[len(fatorX)-1]['value'] += fatorSit[i]['situacoes'][j]['value']

                        j += 1
                i += 1

            #atualiza dados do cálculo 66
            fator = float(getParamByName(constants.PAR_POND66, request.user.id))
            totalFator += round(oportunidade.ponderado * fator,2)
            i=0
            j=0
            for item in fatorCal:
                if oportunidade.lider.id == item['id']:
                    fatorCal[i]['value'] += round(oportunidade.ponderado * fator,2)
                    fatorCal[i]['name'] = oportunidade.lider.first_name

                    j=0
                    for obj in fatorX:
                        if obj['name'] == fatorCal[i]['name']:
                            fatorX[j]['value'] = (fatorX[j]['value'] + fatorCal[i]['value'])/2

                        j += 1

                i += 1

        data = {
            "result" : "ok",
            "data" : {
                "gross": {
                    "total" : totalGross,
                    "items" : gross,
                },
                "ponderado":{
                    "total": totalPonderado,
                    "items": ponderado,
                },
                "situacao":{
                    "total": totalSituacao,
                    "items": fatorSit,
                },
                "fator":{
                    "perc": fator,
                    "total": totalFator,
                    "items": fatorCal,
                },
                "fatorx":{
                    "total": (totalSituacao+totalFator)/2,
                    "items": fatorX,
                },
            },
        }
        context = data
        
        return self.render_to_response(context)
