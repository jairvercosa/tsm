# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView

from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired

class OportunidadeMenu(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização do menu
    """
    template_name = 'oportunidade_menu.html'