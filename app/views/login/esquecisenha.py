from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render

from app.models import CadUsuarios
from app.utils.tokens import gerar_token, traduzir_token
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages

class EsqueciSenhaView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/login/esqueci_senha.html')
    
    def post(self, request, *args, **kwargs):
        
        email = request.POST.get('email')
        
        try:
            user = CadUsuarios.objects.get(email=email)
            
            if user:
                # Gera Token
                token = gerar_token({"idusuario": user.idusuario})
                    
                # Salva no campo tokensenha
                user.tokensenha = token
                user.save()
                
                # Envia email com link de recuperação
                try:
                    subject = 'Link de Reativação'
                    from_email = settings.EMAIL_HOST_USER
                    to = [user.email]
                    
                    link = f"{settings.SITE_PROTOCOL}://{settings.SITE_HOST}/login/esquecisenha/{token}"
                    html_content = render_to_string("email/recuperacao.html", { "link": link })

                    msg = EmailMultiAlternatives(subject, html_content, from_email, to)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except Exception as e:
                    logger.exception("Falha ao enviar email de recuperação")
                
                # Mensagem para o template
                messages.success(request, "Se a conta existir, você receberá um link para redefinir a senha.")
               
        except CadUsuarios.DoesNotExist:
            # Mesmo comportamento para não expor se o e-mail existe
            messages.success(request, "Se a conta existir, você receberá um link para redefinir a senha.")
            
        return render(request, 'pages/login/esqueci_senha.html')