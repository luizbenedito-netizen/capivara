from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from django.contrib import messages
from app.utils.tokens import traduzir_token
from django.conf import settings
from app.models import CadUsuarios
from app.utils.fns import senha_forte
from django.contrib.auth.hashers import make_password, check_password

class ResetarSenhaView(View):

    def valida(self, request):
        
        user = None
        status = True

        token = self.kwargs.get('token')
        ttl = int(getattr(settings, "RECOVERY_TIME_SECONDS", 0))
        
        payload = traduzir_token(token, ttl=ttl)

        if not payload:
            messages.error(request, "Esse link não funciona mais.")
            return (None, False)

        idusuario = payload.get('idusuario')
        if idusuario is None:
            messages.error(request, "Esse link não funciona mais.")
            return (None, False)

        try:
            user = CadUsuarios.objects.get(idusuario=idusuario)
        except CadUsuarios.DoesNotExist:
            messages.error(request, "Usuário inválido.")
            return (None, False)

        if user.tokensenha != token:
            messages.error(request, "Esse link não funciona mais.")
            return (None, False)

        return (user, True)

    def get(self, request, *args, **kwargs):
        user, status = self.valida(request)
        return render(request, 'pages/login/resetar_senha.html')

    def post(self, request, *args, **kwargs):
        user, status = self.valida(request)
        if status and user:
            senha = request.POST.get('senha')

            if not senha_forte(senha):
                messages.error(request, "Formato de Senha Inválido")
            else:
                user.senha = make_password(senha, hasher='bcrypt_sha256')
                user.tokensenha = None
                user.save()
                messages.success(request, "Senha alterada com sucesso!")
        return render(request, 'pages/login/resetar_senha.html')        
