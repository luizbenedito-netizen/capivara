from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from app.models import CadUsuarios
from app.utils.fns import senha_forte

class RegisterView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'pages/login/register.html')

    def post(self, request, *args, **kwargs):

        usuario = request.POST.get('usuario', '').strip()
        email = request.POST.get('email', '').strip().lower()
        senha = request.POST.get('senha', '')

        # Usuário
        if len(usuario) < 3 or len(usuario) > 75:
            messages.error(
                request,
                'O usuário deve ter entre 3 e 75 caracteres.'
            )
            return render(request, 'pages/login/register.html')

        # Email
        if len(email) > 254:
            messages.error(
                request,
                'O email excede o tamanho permitido.'
            )
            return render(request, 'pages/login/register.html')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(
                request,
                'Digite um email válido.'
            )
            return render(request, 'pages/login/register.html')

        # Duplicado
        if CadUsuarios.objects.filter(email=email).exists():
            messages.error(
                request,
                'Este email já está cadastrado.'
            )
            return render(request, 'pages/login/register.html')

        # Senha
        if len(senha) < 12 or len(senha) > 24:

            messages.error(
                request,
                'A senha deve ter entre 12 e 24 caracteres.'
            )

            return render(request, 'pages/login/register.html')

        if not senha_forte(senha):
            messages.error(
                request,
                'A senha é muito fraca.'
            )
            return render(request, 'pages/login/register.html')

        # Cadastro
        user = CadUsuarios.objects.create(
            nome=usuario,
            email=email,
            senha=make_password(senha),
            ativo=True
        )

        # Sessão
        #request.session['user_id'] = user.idusuario
        #request.session['username'] = user.nome
        #request.session['email'] = user.email

        messages.success(
            request,
            'Conta criada com sucesso.'
        )

        return redirect('login')