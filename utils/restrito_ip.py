from flask import request, abort

# Lista de IPs autorizados a acessar certas rotas
IPS_AUTORIZADOS = [
    '127.0.0.1',      # localhost (acesso local)
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


# Exemplo de oque colocar nas rotas:
# @admin_bp.route("/area-restrita")
# @restrito_por_ip
# def painel_super_admin():
#    return render_template("admin/superadmin.html")
