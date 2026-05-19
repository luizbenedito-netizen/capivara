import re
from zxcvbn import zxcvbn
from datetime import datetime
from django.utils import timezone

def senha_forte(senha):

    if not senha:
        return False

    if len(senha) < 12 or len(senha) > 24:
        return False

    score = zxcvbn(senha)['score']

    return score >= 3

def get_greeting():
    hour = timezone.localtime(timezone.now()).hour
    if hour < 13:
        return "Bom dia"
    elif hour < 18:
        return "Boa tarde"
    else:
        return "Boa noite"