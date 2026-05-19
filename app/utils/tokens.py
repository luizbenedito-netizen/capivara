import json
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

def get_fernet():
    """
    Retorna uma instância do Fernet usando a chave definida em settings.FERNET_KEY.
    """
    key = getattr(settings, "FERNET_KEY", None)
    if not key:
        raise RuntimeError("Você PRECISA definir FERNET_KEY no settings.py")
    return Fernet(key)


def gerar_token(payload_dict):
    """
    Recebe um dicionário e retorna um token Fernet (string) criptografado.
    """
    f = get_fernet()
    payload_bytes = json.dumps(payload_dict).encode()
    token = f.encrypt(payload_bytes)
    return token.decode()


def traduzir_token(token, ttl=None):
    """
    Recebe um token Fernet e retorna o dicionário original.
    Se o token estiver inválido, expirado ou ocorrer qualquer erro,
    retorna None.
    """
    f = get_fernet()

    try:
        # Descriptografa com TTL, se fornecido
        if ttl is not None:
            ttl = int(ttl)  # garante tipo correto
            payload_bytes = f.decrypt(token.encode(), ttl=ttl)
        else:
            payload_bytes = f.decrypt(token.encode())

        # Tenta converter o JSON
        return json.loads(payload_bytes)

    except Exception:
        # Qualquer erro → token ilegível
        return None
