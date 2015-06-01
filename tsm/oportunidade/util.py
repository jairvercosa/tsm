# -*- coding: ISO-8859-1 -*-

def calculoTemperatura(respostas):
    """
    Rotina para cálculo da temperatura automática baseado
    nas respostas
    """

    from tsm.oportunidade.models.questao import Questao

    if not respostas:
        raise ValueError("Respostas não repassadas")
    
    questoesId = []
    for item in respostas:
        questoesId.append(item['id'])

    questoes = Questao.objects.filter(id__in=questoesId)

    if not questoes:
        raise ValueError('Questões não foram encontradas')

    total = 0
    for questao in questoes:
        ele = (item for item in respostas if item['id'] == questao.id).next()
        if ele['resposta']:
            total = total + questao.sim
        else:
            total = total + questao.nao

    if total >= 15:
        return "Alta"
    elif total>=10:
        return "Média"
    else:
        return "Baixa"

