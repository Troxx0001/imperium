from flask import request, abort

IPS_AUTORIZADOS = [
    '127.0.0.1',      
    'SEU_IP_PUBLICO_AQUI'
]

def restrito_por_ip(f):
    def wrapper(*args, **kwargs):
        ip = request.remote_addr
        if ip not in IPS_AUTORIZADOS:
            abort(403)
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


