# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.db.models import Q

from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired

class ClienteMenu(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização do menu
    """
    template_name = 'cliente_menu.html'