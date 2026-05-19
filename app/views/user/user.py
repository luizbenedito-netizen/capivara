from django.views import View
from django.shortcuts import render, redirect

class UserView(View):

    def get(self, request, user_id, *args, **kwargs):
        return render(request, 'pages/user/user.html', {
            'active_page': 'user'
        })

    def post(self, request, user_id, *args, **kwargs):
        return True

class UserSettingsView(View):

    def get(self, request, user_id, *args, **kwargs):

        return render(
            request,
            'pages/user/settings.html'
        )