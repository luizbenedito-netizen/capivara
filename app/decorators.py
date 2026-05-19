from django.shortcuts import redirect
from django.http import JsonResponse
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/login')
        return view_func(request, user_id, *args, **kwargs)
    return wrapper

def api_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'Não autorizado'}, status=401)
        return view_func(request, user_id, *args, **kwargs)
    return wrapper