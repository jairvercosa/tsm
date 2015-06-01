from django.http import HttpResponseRedirect

import re

class PasswordChangeMiddleware:
    def process_request(self, request):
        from tsm.acesso.models.usuario import Usuario

        if request.user.is_authenticated() and \
            not re.match(r'^/acesso/sair/?', request.path) and \
            not re.match(r'^/acesso/usuarios/password/?', request.path):

            profile = Usuario.objects.get(pk=request.user.pk)
            if profile.forca_troca_senha:
                return HttpResponseRedirect('/acesso/usuarios/password/')