# -*- coding: ISO-8859-1 -*-
"""
Funções uteis para toda aplicação
"""

def getParam(param):
    """
    Retorna o valor de um parâmetro
    """
    from tsm.core.models.parametro import Parametro
    if not param:
        return None

    parametro = Parametro.objects.filter(nome=param)
    if parametro:
        return parametro[0].valor
    else:
        return None

def getParamByName(param, user_id):
    """
    Retorna o valor de um parâmetro filtrando filiais
    """
    from django.db.models import Q
    from tsm.core.models.parametro import Parametro
    from tsm.acesso.models.usuario import Usuario

    usuario = Usuario.objects.get(id=user_id).filiais.all()
    filiais = usuario

    if not param:
        return None

    parametro = Parametro.objects.filter(nome=param)
    parametro.filter(Q(filial__id__in=Usuario.objects.get(id=user_id).filiais.all())|Q(filial__id__isnull=True))

    if parametro:
        return parametro[0].valor
    else:
        return None

def get_filiais(user_id):
    """
    Retorna as filiais que um usuário pode acessar
    """
    from tsm.core.models.filial import Filial
    from tsm.acesso.models.usuario import Usuario

    if user_id:
        return Filial.objects.filter(id__in=Usuario.objects.get(id=user_id).filiais.all())
    else:
        return None

def format_number(numero):
    """
    Formata o número para o padrão brasileiro
    """

    try:
        contador = 0
        valor_str = ''
        num = numero.__str__()
        if '.' in num:
            valor, decimal = num.split('.')
        else:
            valor = num
            decimal = '00'

        if len(decimal) < 2:
            decimal = decimal + '0'

        tamanho = len(valor)
        while tamanho > 0:
            valor_str = valor_str + valor[tamanho-1]
            contador += 1
            if contador == 3 and tamanho > 1:
                valor_str = valor_str + ','
                contador = 0
            tamanho -= 1

        tamanho = len(valor_str)
        str_valor = ''
        while tamanho > 0:
            str_valor = str_valor + valor_str[tamanho-1]
            tamanho -= 1

        return "%s.%s" % (str_valor,decimal)
    except:
        return "Erro. Nao foi possivel converter o valor enviado."

def isDiaUtil(dateParam,user):
    """
    Verifica se um dia é útil

    @return boolean, string
    """
    from datetime import date
    from django.db.models import Q

    from tsm.core import constants
    from tsm.core.models.feriado import Feriado
    from tsm.acesso.models.usuario import Usuario

    #Valida fim de semana
    dayWeek = dateParam.weekday()
    days_week_dict = dict(constants.DAYS_WEEK_BR)
    sabado = eval(getParamByName(constants.PAR_SABADO,user.id))
    domingo = eval(getParamByName(constants.PAR_DOMINGO,user.id))
    if not sabado and days_week_dict[dayWeek] == 'Sábado':
        return False, 'Sábado não é considerado dia útil.'

    if not domingo and days_week_dict[dayWeek] == 'Domingo':
        return False, 'Domingo não é considerado dia útil.'
    
    #Valida feriados
    hoje = date.today()
    feriados = Feriado.objects.filter(data__day=dateParam.day,data__month=dateParam.month)
    feriados = feriados.filter(Q(data__year=dateParam.year)|Q(is_repeat=True))
    feriados = feriados.filter(Q(filial__id__in=Usuario.objects.get(id=user.id).filiais.all())|Q(filial__id__isnull=True))
    
    if feriados:
        return False, feriados[0].nome

    return True, ''




